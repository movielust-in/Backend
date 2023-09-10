from os import environ
from marshmallow import EXCLUDE, Schema, validate
from marshmallow.fields import (
    String,
    Integer,
    Boolean,
)


class Env(Schema):
    FLASK_DEBUG = String(
        required=True,
        error_messages={
            "required": "FLASK_DEBUG variable is not configured",
            "OneOf": "FLASK_DEBUG can only take value of 'production' or 'development'",
        },
        validate=validate.OneOf(
            ["production", "development"]
        ),
    )
    SECRET = String(
        required=True,
        error_messages={
            "required": "SECRET variable is not configured"
        },
    )
    TMDB_KEY = String(
        required=True,
        error_messages={
            "required": "TMDB_KEY variable is not configured"
        },
    )
    MAIL_SERVER = String(
        required=True,
        error_messages={
            "required": "MAIL_SERVER variable is not configured"
        },
    )
    MAIL_EMAIL = String(
        required=True,
        error_messages={
            "required": "MAIL_EMAIL variable is not configured"
        },
    )
    MAIL_PASSWORD = String(
        required=True,
        error_messages={
            "required": "MAIL_PASSWORD variable is not configured"
        },
    )
    MAIL_PORT = Integer(
        required=True,
        error_messages={
            "required": "MAIL_PORT variable is not configured"
        },
    )
    MAIL_USE_SSL = Boolean(
        required=True,
        error_messages={
            "required": "MAIL_USE_SSL variable is not configured"
        },
    )
    MAIL_USE_TLS = Boolean(
        required=True,
        error_messages={
            "required": "MAIL_USE_TLS variable is not configured"
        },
    )
    DATABASE_URL = String(
        required=True,
        error_messages={
            "required": "DATABASE_URL variable is not configured"
        },
    )
    ADMIN_SECRET = String(
        required=True,
        error_messages={
            "required": "ADMIN_SECRET variable is not configured"
        },
    )


def validate_env():
    env = dict(environ)
    Env().load(env, unknown=EXCLUDE)
