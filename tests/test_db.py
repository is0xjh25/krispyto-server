# tests/test_db.py

import pytest
from sqlalchemy import text, inspect
from config.settings import Config
from app import create_app, db 

@pytest.fixture
def app():
    app = create_app(Config())
    with app.app_context():
        yield app

def test_database_connection(app):
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                assert result.scalar() == 1
        except Exception as e:
            assert False, f"Error connecting to the database: {e}"

def test_database_empty(app):
    try:
        with app.app_context():
            inspector = inspect(db.engine)
            table_names = inspector.get_table_names()
            # Exclude "alembic_version" table
            table_names = [table for table in table_names if table != "alembic_version"]
            assert table_names
    except Exception as e:
        assert False, f"Error connecting to the database: {e}"

def test_first_table_has_data(app):
    try:
        with app.app_context():
            inspector = inspect(db.engine)
            table_names = inspector.get_table_names()
            # Exclude "alembic_version" table
            table_names = [table for table in table_names if table != "alembic_version"]
            assert table_names

            # Check if the first table has data
            if table_names:
                first_table_name = table_names[0]
                query_result = db.session.execute(f"SELECT 1 FROM {first_table_name} LIMIT 1").fetchone()
                assert query_result is not None
    except Exception as e:
        assert False, f"Error connecting to the database: {e}"