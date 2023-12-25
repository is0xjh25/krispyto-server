# app/__init__.py

from flask import Flask
from config.settings import Config
from flask_migrate import Migrate
from utilities.helper import inspect_database
from app.models import db, Currency, Record
from app import routes

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Check the status of the database only if it's not the testing environment
    inspect_database(app) if not app.config['TESTING'] else None  # Comment out before migration

    app.register_blueprint(routes.bp)

    return app