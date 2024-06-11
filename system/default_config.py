import os

from dotenv import load_dotenv

load_dotenv(".env", verbose=True)
DEBUG = True
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get("APP_SECRET_KEY")
PROPAGATE_EXCEPTIONS = True
