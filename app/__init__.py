# app/__init__.py

from flask import Flask
from config.settings import Config
from flask_migrate import Migrate
from utils.helper import inspect_database
from app.models import db, Currency, Record

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Check the status of database
    inspect_database(app)

    return app