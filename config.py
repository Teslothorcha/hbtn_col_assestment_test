"""Class-based Flask app configuration."""
import os
from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Configuration from environment variables."""

    SECRET_KEY = environ.get("SECRET_KEY", 'default-key')
    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_APP = "wsgi.py"
    # API
    BEST_BUY_API_KEY = environ.get("BEST_BUY_API_KEY")

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False