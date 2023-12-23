# app.py

from app import create_app, db
from config.settings import Config

app = create_app(config_class=Config)

if __name__ == '__main__':
    app.run(debug=True)