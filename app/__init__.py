from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

application = Flask(__name__)
application.config.from_object(Config)
database = SQLAlchemy(application)
migration = Migrate(application, database)
login = LoginManager(application)
login.login_view = "login"


from app import routes, models
