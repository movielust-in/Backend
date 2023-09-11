"""Flask App"""
from http.client import HTTPException
from os import environ

from flask_cors import CORS
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from werkzeug.exceptions import (
    BadRequest,
    NotFound,
)
from flask import Flask, jsonify


from src.routes import routes

from .config import config as app_config


def create_app():
    """Return Flask App"""

    load_dotenv()

    app_env = get_environment()

    mongo = MongoClient(
        app_config[app_env].DATABASE_URL
    )

    app = Flask(app_config[app_env].APP_NAME)

    db = mongo.moviebase

    app.db = db

    app.config.from_object(app_config[app_env])

    CORS(app)

    app.register_blueprint(
        routes, url_prefix="/v1"
    )

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return (
            jsonify(
                error=str(error),
                message="Bad Request",
            ),
            400,
        )

    @app.errorhandler(NotFound)
    def handle_not_found(error):
        return (
            jsonify(
                error=str(error),
                message="Not found!",
            ),
            404,
        )

    @app.errorhandler(Exception)
    def handle_not_foun(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error=str(e)), code

    return app


def get_environment():
    """Returns app environment"""
    return (
        environ.get("FLASK_DEBUG") or "production"
    )
