from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt

from .config import config

db = SQLAlchemy()
migrate = Migrate()
JWT_SECRETKEY = bcrypt.hashpw(b'itsAs3cr34tkeyforJWT', bcrypt.gensalt())


def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])

    db.init_app(app)
    migrate.init_app(app, db)

    return app
