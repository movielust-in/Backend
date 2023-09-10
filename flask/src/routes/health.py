"""Health Routes"""
import re
from flask import (
    Blueprint,
    jsonify,
    current_app as app,
    request,
)

from src.middlewares.validator import validate
from src.utils.constants import Constants
from src.validation import auth_validation

health = Blueprint("health", __name__)


@health.route("/", methods=["GET"])
def health_check():
    return jsonify(message="Server running.")


@health.route(
    "/submit-contact-us", methods=["POST"]
)
@validate(auth_validation.UserRegister())
def submit_contact_us():
    try:
        req = request.get_json()

        if not req:
            return (
                jsonify(
                    success=False,
                    message="Invalid Input!",
                ),
                400,
            )

        if not (
            "name" in req
            and "email" in req
            and "message" in req
        ):
            return (
                jsonify(
                    success=False,
                    message="Invalid Input!",
                ),
                400,
            )

        name = req["name"]
        email = req["email"]
        message = req["message"]

        if (
            not Constants.SPECIAL_CHARS.search(
                name
            )
            is None
        ):
            return (
                jsonify(
                    success=False,
                    message="Invalid Name!",
                ),
                400,
            )

        if not re.fullmatch(
            Constants.EMAIL_REGEX, email
        ):
            return (
                jsonify(
                    success=False,
                    message="Invalid Email!",
                ),
                400,
            )

        app.db.queries.insert_one(
            {
                "name": name,
                "email": email,
                "message": message,
            }
        )

        return (
            jsonify(
                success=True,
                message="Message Sent.",
            ),
            201,
        )

    except:
        return (
            jsonify(
                success=False,
                message="Something Went wrong. Please try again!",
            ),
            500,
        )
