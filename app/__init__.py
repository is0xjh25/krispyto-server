# app/__init__.py

from flask import Flask
from config.settings import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions within the app context
    db.init_app(app)
    migrate.init_app(app, db)

    # Import routes and models here to avoid circular imports
    from app import routes, models

    return app