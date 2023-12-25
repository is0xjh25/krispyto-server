# app/routes.py

import re
from flask import Blueprint, jsonify, request
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models import Currency, Record
from app import db

bp = Blueprint('main', __name__)

date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

# Define a before_request function to check for 404 errors
@bp.before_request
def check_for_404():
    if request.endpoint is None:
        return jsonify({"error": "Bad request."}), 404

# Route for getting crypto records
@bp.route('/dashboard', methods=['GET'])
def search_crypto_prices():
    # Extract parameters from the request
    crypto_id = request.args.get('id')
    date = request.args.get('date')
    order_by = request.args.get('order_by')
    order_type = request.args.get('order_type')

    # Define valid values for order_by and order_type
    valid_order_by_values = ['crypto', 'price', '24h', '7d', '1m', '24h-volume', 'market_cap']
    valid_order_type_values = ['asc', 'desc']

    # Validate parameters
    if not all([crypto_id, date, order_by, order_type]):
        return jsonify({"error": "Missing parameter(s)."}), 400
    # Validate 'id' (crypto_id)
    if not isinstance(crypto_id, str):
        return jsonify({"error": "Invalid data type for 'id'. 'id' must be a string."}), 400
    # Validate 'date' format
    if not date_pattern.match(date):
        return jsonify({"error": "Invalid format for 'date'. Please use the format YYYY-MM-DD."}), 400
    # Validate 'order_by'
    if order_by not in valid_order_by_values:
        return jsonify({"error": "Invalid value for 'order_by'."}), 400
    # Validate 'order_type'
    if order_type not in valid_order_type_values:
        return jsonify({"error": "Invalid value for 'order_type'."}), 400

    # Read the crypto(s) for the dashboard
    crypto = read_crypto_id(crypto_id)

    # Verify that there are records for the previous 30 days
    if not verify_date(crypto, date):
        return jsonify({"warning": "Invalid value for 'date'. No records for the previous 30 days."}), 204

    processed_crypto = process_crypto(crypto, date)
    ordered_crypto = order_crypto(processed_crypto, order_by, order_type)

    return jsonify(ordered_crypto), 200

# Route for searching crypto existence in the database
@bp.route('/search', methods=['GET'])
def search_crypto_exists():
    # Extract parameter from the request
    crypto_name = request.args.get('name')

    # Validate that crypto_name is a string
    if not isinstance(crypto_name, str):
        return jsonify({"error": "Invalid data type for 'name'. 'name' must be a string."}), 400

    # Find the Currency with the matching name (case-insensitive)
    currency = Currency.query.filter(func.lower(Currency.name) == func.lower(crypto_name)).first()

    # If not found by name, try finding by symbol (case-insensitive)
    if not currency:
        currency = Currency.query.filter(func.lower(Currency.symbol) == func.lower(crypto_name)).first()

    # Check if a currency is found
    if currency:
        response_data = {"name": currency.name, "symbol": currency.symbol}
        return jsonify(response_data), 200
    else:
        return jsonify({"error": f"No currency found with name or symbol '{crypto_name}'."}), 204

# Extracts the list of crypto symbols based on the provided crypto_id
def read_crypto_id(crypto_id):
    crypto_list = []
    if crypto_id == 'all':
        all_currencies = Currency.query.all()
        crypto_list = [currency.symbol for currency in all_currencies]
    else:
        crypto_ids = crypto_id.split(',')
        crypto_list.extend(crypto_ids)
    return crypto_list

# Verifies if there are records for the previous 30 days based on the provided date
def verify_date(crypto, date):
    try:
        input_date = datetime.strptime(date, '%Y-%m-%d')
        start_date = input_date - timedelta(days=30)

        for symbol in crypto:
            currency_info = Currency.query.filter(func.lower(Currency.symbol) == func.lower(symbol)).first()

            if currency_info:
                records_in_range = Record.query.filter(
                    Record.currency_id == currency_info.id,
                    Record.date >= start_date,
                    Record.date <= input_date
                ).all()

                # If any crypto has fewer than 30 records, return False
                if len(records_in_range) < 30:
                    return False
            else:
                # If the currency symbol is not found, consider it a failure
                return False

        # If all cryptos have 30 or more records, return True
        return True
    
    except ValueError:
        # Handle invalid date format
        return False

# Processes crypto data for the specified symbols and date
def process_crypto(crypto, date):
    crypto_data = []

    for symbol in crypto:
        try:
            currency = Currency.query.filter(func.lower(Currency.symbol).ilike(func.lower(symbol))).first()

            if currency:
                # Find the associated records for the previous 30 days
                end_date = datetime.strptime(date, '%Y-%m-%d')
                start_date = end_date - timedelta(days=30)
                previous_records = Record.query.filter(
                    Record.currency_id == currency.id,
                    Record.date >= start_date,
                    Record.date <= end_date
                ).all()

                if len(previous_records) >= 30:
                    # Calculate the required values
                    latest_record = previous_records[-1]
                    price = latest_record.close
                    volume = latest_record.volume
                    market_cap = latest_record.marketcap

                    # Calculate percentage changes
                    price_change_24h = ((latest_record.close - previous_records[-2].close) / previous_records[-2].close) * 100
                    price_change_7d = ((latest_record.close - previous_records[-8].close) / previous_records[-8].close) * 100
                    price_change_1m = ((latest_record.close - previous_records[0].close) / previous_records[0].close) * 100

                    # Create a dictionary for the current cryptocurrency
                    crypto_entry = {
                        'crypto': currency.name,
                        'symbol': symbol,
                        'price': price,
                        '24h': price_change_24h,
                        '7d': price_change_7d,
                        '1m': price_change_1m,
                        '24h-volume': volume,
                        'market-cap': market_cap
                    }

                    # Append the dictionary to the array
                    crypto_data.append(crypto_entry)
            #     else:
            #         print(f"[Server] Not enough records for Symbol: {symbol}")
            # else:
            #     print(f"[Server] No currency found for Symbol: {symbol}")
        except Exception as e:
            # Handle any other exceptions that might occur during the process
            print(f"[Server] An error occurred for Symbol: {symbol}. Error: {str(e)}")

    return crypto_data

# Orders the processed_crypto data based on specified criteria
def order_crypto(processed_crypto, order_by, order_type):
    # Define a mapping of order_by values to corresponding fields in the processed_crypto data
    order_by_mapping = {
        'crypto': 'crypto',
        'price': 'price',
        '24h': '24h',
        '7d': '7d',
        '1m': '1m',
        '24h-volume': '24h-volume',
        'market-cap': 'market-cap'
    }

    # Define a lambda function to extract the specified field for sorting
    key_function = lambda x: x[order_by_mapping[order_by]]

    # Determine the reverse flag based on order_type
    reverse_flag = order_type.lower() == 'desc'

    # Sort the processed_crypto data based on the specified criteria
    ordered_crypto = sorted(processed_crypto, key=key_function, reverse=reverse_flag)

    return ordered_crypto