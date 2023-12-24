# tests/test_db.py

import pytest
from sqlalchemy import text, inspect
from config.settings import Config
from app import create_app, db 

# Fixture to create the Flask app for testing
@pytest.fixture(scope='session')
def app():
    app = create_app(Config())
    with app.app_context():
        yield app

# Test to check if the database connection is successful
def test_database_connection(app):
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                assert result.scalar() == 1
        except Exception as e:
            assert False, f"Error connecting to the database: {e}"

# Test to check if the database is not empty
def test_database_empty(app):
    try:
        with app.app_context():
            inspector = inspect(db.engine)
            # Exclude "alembic_version" table
            table_names = [table for table in inspector.get_table_names() if table != "alembic_version"]
            assert table_names
    except Exception as e:
        assert False, f"Error connecting to the database: {e}"

# Test to check if the first table has data
def test_first_table_has_data(app):
    try:
        with app.app_context():
            inspector = inspect(db.engine)
            # Exclude "alembic_version" table
            table_names = [table for table in inspector.get_table_names() if table != "alembic_version"]
            assert table_names

            if table_names:
                first_table_name = table_names[0]
                query_result = db.session.execute(text(f"SELECT 1 FROM {first_table_name} LIMIT 1")).fetchone()
                assert query_result is not None
    except Exception as e:
        assert False, f"Error connecting to the database: {e}"