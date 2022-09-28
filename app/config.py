import os
from pathlib import Path,PurePath

from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
pathlibBaseDir = Path.cwd()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'out_of_ur_range'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bikerental.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]
    PRICE = 5