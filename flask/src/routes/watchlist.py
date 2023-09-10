from http import HTTPStatus
from flask import (
    Blueprint,
    current_app as app,
    request,
    jsonify,
)
from src.middlewares.token_verification import (
    token_required,
)

watchlist = Blueprint("Watchlist", __name__)


@watchlist.route(
    "/watchlist/add", methods=["POST"]
)
@token_required
def add_to_watchlist(userObj):
    try:
        req = request.get_json()

        if (
            not req
            or req["content_id"] is None
            or req["type"] is None
        ):
            return (
                jsonify(
                    error=True,
                    message=HTTPStatus.BAD_REQUEST.phrase,
                ),
                HTTPStatus.BAD_REQUEST.value,
            )

        already_exists = app.db.user.find_one(
            {
                "email": userObj["email"],
                "watchlist": {
                    "$elemMatch": {
                        "content_id": req[
                            "content_id"
                        ],
                        "type": req["type"],
                    }
                },
            }
        )

        if already_exists is None:
            app.db.user.update_one(
                {"email": userObj["email"]},
                {
                    "$push": {
                        "watchlist": {
                            "content_id": req[
                                "content_id"
                            ],
                            "type": req["type"],
                        }
                    }
                },
            )
            return (
                jsonify(
                    success=True,
                    message=req["type"]
                    + " added to watchlist.",
                ),
                201,
            )

        return (
            jsonify(
                success=False,
                message="Already Exists",
            ),
            HTTPStatus.NOT_MODIFIED.value,
        )

    except Exception:
        return (
            jsonify(
                error=True,
                message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


# Retrieves users watchlist
@watchlist.route(
    "/watchlist/get", methods=["GET"]
)
@token_required
def fetch_watchlist(userObj):
    try:
        email = userObj["email"]
        data = app.db.user.find_one(
            {"email": email}, {"watchlist": 1}
        )
        if data is not None:
            return (
                jsonify(
                    success=True,
                    message="Watchlist Retrieved.",
                    results=data["watchlist"],
                ),
                200,
            )

        return (
            jsonify(
                success=True,
                message="Watchlist Empty.",
            ),
            200,
        )
    except Exception:
        return (
            jsonify(
                error=True,
                message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


# removes show or movie from users watchlist
@watchlist.route(
    "/watchlist/remove", methods=["DELETE"]
)
@token_required
def del_from_watchlist(userObj):
    try:
        req = request.get_json()

        if not req:
            return (
                jsonify(
                    success=False,
                    message="No input",
                ),
                HTTPStatus.BAD_REQUEST.value,
            )

        if not (
            "content_id" in req and "type" in req
        ):
            return (
                jsonify(
                    success=False,
                    message="Invalid request",
                ),
                HTTPStatus.BAD_REQUEST.value,
            )

        email = userObj["email"]

        app.db.user.update_one(
            {"email": email},
            {
                "$pull": {
                    "watchlist": {
                        "content_id": str(
                            req["content_id"]
                        ),
                        "type": req["type"],
                    }
                }
            },
        )

        app.db.user.update_one(
            {"email": email},
            {
                "$pull": {
                    "watchlist": {
                        "content_id": req[
                            "content_id"
                        ],
                        "type": req["type"],
                    }
                }
            },
        )

        return (
            jsonify(
                success=True,
                message="Removed from Watchlist.",
            ),
            HTTPStatus.OK.value,
        )
    except Exception:
        return (
            jsonify(
                error=True,
                message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
