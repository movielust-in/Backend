"""Flask App"""
from http.client import HTTPException
import logging.config
from os import environ

from flask_cors import CORS
from flask_talisman import Talisman
from flask_compress import Compress
from flask_mail import Mail
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from werkzeug.exceptions import (
    BadRequest,
    NotFound,
)
from flask import Flask, jsonify
import sentry_sdk
from sentry_sdk.integrations.flask import (
    FlaskIntegration,
)
from src.routes import routes

from .config import config as app_config


def create_app():
    """Return Flask App"""
    load_dotenv()

    # sentry_sdk.init(
    #     dsn="https://7f99f1d17bde40398451dffcb236b2a8@o1358835.ingest.sentry.io/6646140",
    #     integrations=[
    #         FlaskIntegration(),
    #     ],
    #     # Set traces_sample_rate to 1.0 to capture 100%
    #     # of transactions for performance monitoring.
    #     # We recommend adjusting this value in production.
    #     traces_sample_rate=1.0,
    # )

    app_env = get_environment()

    # logging.config.dictConfig(app_config[app_env].LOGGING)

    mongo = MongoClient(
        app_config[app_env].DATABASE_URL
    )

    app = Flask(app_config[app_env].APP_NAME)

    db = mongo.moviebase

    app.db = db

    app.config.from_object(app_config[app_env])

    app.mail = Mail(app)

    CORS(app)

    Talisman(app)

    Compress(app)

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

    @app.route("/debug-sentry", methods=["GET"])
    def error_route():
        div = 1 / 0
        return jsonify(error=div), 500

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
