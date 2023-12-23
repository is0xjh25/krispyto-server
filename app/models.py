# app/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    symbol = db.Column(db.String(10))

    # Define a relationship to Record
    records = db.relationship('Record', back_populates='currency')

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    date = db.Column(db.DateTime)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    open = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    marketcap = db.Column(db.Float)

    # Define a relationship to Currency
    currency = db.relationship('Currency', back_populates='records')