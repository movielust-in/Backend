from functools import wraps
from os import environ
from jwt import decode, InvalidTokenError
from flask import request, jsonify


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "Authorization" in request.headers:
            (
                bearer,
                _,
                token,
            ) = request.headers.get(
                "Authorization"
            ).partition(
                " "
            )
            if bearer != "Bearer":
                token = None
        # return 401 if token is missing
        if not token:
            return (
                jsonify(
                    {"message": "Unauthorized!"}
                ),
                401,
            )

        try:
            # decoding the payload to fetch the stored details
            data = decode(
                token,
                environ.get("SECRET"),
                algorithms=["HS256"],
                issuer="Movielust",
                verify=True,
            )
        except InvalidTokenError:
            return (
                jsonify(
                    {
                        "message": "Token is invalid !!"
                    }
                ),
                401,
            )
        # returns the current logged in users contex to the routes
        return f(
            {
                "id": data["id"],
                "email": data["email"],
            },
            *args,
            **kwargs
        )

    return decorated
