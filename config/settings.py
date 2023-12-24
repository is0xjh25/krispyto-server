# config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_ENDPOINT = os.getenv("DB_ENDPOINT")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    GOOGLE_FILE_ID = os.getenv("GOOGLE_FILE_ID")
    CSV_FILE_FOLDER = os.getenv("CSV_FILE_FOLDER")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'