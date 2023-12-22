import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_ENDPOINT = os.getenv("DB_ENDPOINT")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy