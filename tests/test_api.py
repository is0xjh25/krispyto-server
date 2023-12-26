# tests/test_api.py

import pytest
from config.settings import TestConfig
from datetime import datetime, timedelta
from app.models import Currency, Record
from app import create_app, db

# Fixture to create the Flask app for testing
@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig())
    with app.app_context():
        db.create_all()

        # Add test data for Currency
        bitcoin = Currency(name='Bitcoin', symbol='BTC')
        ethereum = Currency(name='Ethereum', symbol='ETH')
        db.session.add_all([bitcoin, ethereum])
        db.session.commit()

        # Add test data for Record
        current_time = datetime.utcnow()
        thirty_days_ago = current_time - timedelta(days=30)
        bitcoin_records = [Record(currency_id=bitcoin.id, date=current_time - timedelta(days=i), close=100 + i, volume=1000 + i, marketcap=10000 + i) for i in range(31)]
        ethereum_records = [Record(currency_id=ethereum.id, date=current_time - timedelta(days=i), close=50 + i, volume=500 + i, marketcap=5000 + i) for i in range(31)]
        db.session.add_all(bitcoin_records + ethereum_records)
        db.session.commit()

        yield app

# Fixture to create the test client
@pytest.fixture(scope='session')
def client(app):
    with app.test_client() as client:
        yield client

# Test for searching crypto prices for all cryptocurrencies
def test_search_crypto_prices_all(client):
    current_date = datetime.now().strftime('%Y-%m-%d')
    response = client.get(f'/dashboard?id=all&date={current_date}&order_by=price&order_type=asc')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert all(key in response.json[0] for key in ['crypto', 'price', '24h', '7d', '1m', '24h-volume', 'market-cap'])
    assert response.json[0]['crypto'] == 'Ethereum'

# Test for searching crypto prices for a specific cryptocurrency (favorite)
def test_search_crypto_prices_favourite(client):
    current_date = datetime.now().strftime('%Y-%m-%d')
    response = client.get(f'/dashboard?id=btc&date={current_date}&order_by=price&order_type=asc')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert all(key in response.json[0] for key in ['crypto', 'price', '24h', '7d', '1m', '24h-volume', 'market-cap'])

# Test for searching crypto prices with invalid parameters
def test_search_crypto_prices_not_found(client):
    response = client.get('/dashboard?id=xxx,btc&date=1999-10-23&order_by=price&order_type=asc')
    assert response.status_code == 404

# Test for searching crypto existence by name
def test_search_crypto_exists_name(client):
    response = client.get('/search?name=bitcoin')
    assert response.status_code == 200
    assert 'name' in response.json
    assert 'symbol' in response.json

# Test for searching crypto existence by symbol
def test_search_crypto_exists_symbol(client):
    response = client.get('/search?name=btc')
    assert response.status_code == 200
    assert 'name' in response.json
    assert 'symbol' in response.json

# Test for searching non-existing crypto by name
def test_search_crypto_exists_name_not_found(client):
    response = client.get('/search?name=xxx')
    assert response.status_code == 404

# Test for handling bad request
def test_bad_request(client):
    response = client.get('/xxx')
    assert response.status_code == 404