from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

application = Flask(__name__)
application.config.from_object(Config)
database = SQLAlchemy(application)
migration = Migrate(application, database)


from app import routes, models
