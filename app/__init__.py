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

    # Check the status of the database only if it's not the testing environment
    if not app.config['TESTING']:
        inspect_database(app)  # Comment out before migration

    # Import and register your routes
    from app import routes
    app.register_blueprint(routes.bp)

    return app