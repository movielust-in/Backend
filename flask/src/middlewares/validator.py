from functools import wraps
from http import HTTPStatus
from marshmallow import Schema, ValidationError
from flask import request, jsonify


def validate(schema: Schema):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.method == "GET":
                raise Exception(
                    "Validate middleware is can not be used on GET methods! "
                )
            if (
                "Content-Type"
                not in request.headers
                or request.headers["Content-Type"]
                != "application/json"
            ):
                return (
                    jsonify(
                        error=True,
                        message="Content type does not match application/json",
                    ),
                    415,
                )
            try:
                json = request.get_json()

                if json is None:
                    return (
                        jsonify(
                            error=False,
                            message="No body in request!",
                        ),
                        HTTPStatus.BAD_REQUEST.value,
                    )

                schema.load(json)

            except ValidationError as validation_err:
                return (
                    jsonify(
                        error=True,
                        message=validation_err.messages,
                    ),
                    HTTPStatus.BAD_REQUEST.value,
                )

            except Exception as err:
                print(
                    "**************************************"
                )
                print(err)
                error = {
                    "success": False,
                    "messages": HTTPStatus.BAD_REQUEST.phrase,
                    "error": err,
                }
                return (
                    jsonify(error),
                    HTTPStatus.BAD_REQUEST.value,
                )
            return fn(*args, **kwargs)

        return wrapper

    return decorator
