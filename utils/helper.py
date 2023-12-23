# utils/helper.py

import os
import zipfile
import pandas as pd
from google_drive_downloader import GoogleDriveDownloader as gdd
from sqlalchemy import text, inspect, create_engine
from datetime import datetime
from app.models import db, Currency, Record

# Download the zip file from Google Drive
def download_and_extract_zip(file_id, dest_path):
    print("[Server] Data downloading")
    zip_file_path = dest_path + 'crypto.zip'

    # Download the zip file from Google Drive
    gdd.download_file_from_google_drive(file_id=file_id, dest_path=zip_file_path, unzip=True)

    # Print the list of files in the extracted directory
    for root, dirs, files in os.walk(dest_path):
        for file in files:
            print(os.path.join(root, file))

    # Delete the zip file after extraction
    os.remove(zip_file_path)

    print("[Server] Files download completed")

# Read downloaded file and upload to database
def read_files_and_upload(app, src_path):
    try:
        with app.app_context():
            # Delete each record
            # remove_all_data()

            # Iterate through each file in the specified directory
            for filename in os.listdir(src_path):
                file_path = os.path.join(src_path, filename)

                # Read the CSV file into a DataFrame, skipping the first row
                df = pd.read_csv(file_path, delimiter=',', skiprows=1)
                currency_name = df.iloc[0, 1]  # Assuming the currency name is in the second column
                currency_symbol = df.iloc[0, 2]  # Assuming the currency symbol is in the third column

                # Add currency
                currency = db.session.query(Currency).filter_by(name=currency_name).first()
                if not currency:
                    currency = Currency(name=currency_name, symbol=currency_symbol)
                    db.session.add(currency)
                    db.session.commit()

                for index, row in df.iterrows():
                    # Create a Record and associate it with the corresponding currency
                    record = Record(
                        currency_id=currency.id,
                        date=datetime.strptime(row.iloc[3], '%Y-%m-%d %H:%M:%S'),
                        high=float(row.iloc[4]),
                        low=float(row.iloc[5]),
                        open=float(row.iloc[6]),
                        close=float(row.iloc[7]),
                        volume=float(row.iloc[8]),
                        marketcap=float(row.iloc[9])
                    )

                    # Add the record to the session
                    db.session.add(record)

            # Commit changes to the database after processing all files
            db.session.commit()

            print("[Server] Data has been uploaded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Inspecting the database
def inspect_database(app):
    print("[Server] Checking database status")

    with app.app_context():
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()

        # Exclude "alembic_version" table
        table_names = [table for table in table_names if table != "alembic_version"]
        # Check if there are tables
        if not table_names:
            raise Exception("No tables found. Please run migrations first.")

        # Continue with other checks or actions if needed
        print("[Server] Tables found. Proceeding with other checks if needed.")

        # Loop through all tables and check if each table has at least one row of data
        for table_name in table_names:
            query = text(f"SELECT 1 FROM {table_name} LIMIT 1")
            query_result = db.session.execute(query).fetchone()
            if query_result is None:
                # Download and extract the data from Google Drive
                download_and_extract_zip(app.config['GOOGLE_FILE_ID'], app.config['CSV_FILE_FOLDER'])
                # Process data
                read_files_and_upload(app, app.config['CSV_FILE_FOLDER'])
                break

    print("[Server] Inspection completed")

def remove_all_data():
    try:
        # Query all currencies
        currencies = Currency.query.all()

        # Delete each currency along with associated records
        for currency in currencies:
            # Query records associated with the current currency
            records_to_remove = Record.query.filter_by(currency_id=currency.id).all()

            # Delete each record
            for record in records_to_remove:
                db.session.delete(record)

            # Delete the currency itself
            db.session.delete(currency)

        # Commit changes to the database
        db.session.commit()

        print("[Server] All currencies and associated records have been removed.")
    except Exception as e:
        print(f"An error occurred: {e}")

