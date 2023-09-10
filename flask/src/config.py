"""Flask App Configuration"""
from os import environ, path
from dotenv import load_dotenv

from src.utils.validate_env import validate_env

basedir = path.abspath(
    path.join(path.dirname(__file__), "..")
)
# loading env vars from .env file
load_dotenv()

validate_env()


class BaseConfig(object):
    """Base config class."""

    APP_NAME = "Movielust"
    ORIGINS = ["*"]
    EMAIL_CHARSET = "UTF-8"
    TMDB_KEY = environ.get("TMDB_KEY")
    LOG_INFO_FILE = path.join(
        basedir, "log", "info.log"
    )
    MAIL_SERVER = environ.get("MAIL_SERVER")
    MAIL_PORT = int(environ.get("MAIL_PORT"))
    MAIL_USERNAME = environ.get("MAIL_EMAIL")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = environ.get(
        "MAIL_EMAIL"
    )
    MAIL_DEBUG = False
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class Development(BaseConfig):
    """Development config."""

    DEBUG = True
    ENV = "dev"
    DATABASE_URL = environ.get("DATABASE_URL")


class Staging(BaseConfig):
    """Staging config."""

    DEBUG = True
    ENV = "staging"
    DATABASE_URL = environ.get("DATABASE_URL")


class Production(BaseConfig):
    """Production config"""

    DEBUG = False
    ENV = "production"
    DATABASE_URL = environ.get("DATABASE_URL")


config = {
    "development": Development,
    "staging": Staging,
    "production": Production,
}
