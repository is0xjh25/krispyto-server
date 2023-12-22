# tests/test_db.py

from sqlalchemy import text
from config.settings import Config
from app import app, db

def test_database_connection():
    app_config = Config()
    db_uri = app_config.SQLALCHEMY_DATABASE_URI

    with app.app_context():
        try:
            # Attempt to execute a simple query to check the database connection
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                assert result.scalar() == 1
            print("Database connection successful!")
        except Exception as e:
            assert False, f"Error connecting to the database: {e}"