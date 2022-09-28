from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap
import logging,os
from logging.handlers import SMTPHandler,RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager

bikerental = Flask(__name__)

## Database integration
bikerental.config.from_object(Config)
db = SQLAlchemy(bikerental)
migrate = Migrate(bikerental, db)

## Registering bootstrap with this flask project
Bootstrap(bikerental)

## Setting date time moment library
moment = Moment(bikerental)

## Login implementations
login = LoginManager(bikerental)
login.login_view = 'login'

##register ajax apis
from app.api import bp as api_bp
bikerental.register_blueprint(api_bp, url_prefix='/api')

if not bikerental.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/bikerental.log', maxBytes=10240,
                                       backupCount=10)
    
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    
    file_handler.setLevel(logging.INFO)
    bikerental.logger.addHandler(file_handler)

    bikerental.logger.setLevel(logging.INFO)
    bikerental.logger.info('PEDAL startup')

from app import routes,models
