from datetime import datetime, timezone
from http.client import BAD_REQUEST, CONFLICT
from flask import (
    Blueprint,
    current_app as app,
    request,
    jsonify,
)

from src.middlewares.token_verification import (
    token_required,
)

users = Blueprint("users", __name__)


@users.route("/profile", methods=["GET"])
@token_required
def getuserprofile(userObj):
    try:
        user_found = app.db.user.find_one(
            {"email": userObj["email"]},
            {
                "id": 1,
                "name": 1,
                "email": 1,
                "profile": 1,
            },
        )
        if user_found:
            app.db.user.update_one(
                {"email": user_found["email"]},
                {
                    "$push": {
                        "visits": datetime.now(
                            timezone.utc
                        )
                    }
                },
                upsert=True,
            )
            return (
                jsonify(
                    success=True,
                    message="Login Ok.",
                    email=user_found["email"],
                    profile=user_found["profile"],
                    name=user_found["name"],
                    id=user_found["id"],
                ),
                200,
            )

        return (
            jsonify(
                success=False,
                message="Unauthorized",
            ),
            401,
        )

    except Exception:
        return (
            jsonify(
                success=False,
                message="Something Went Wrong! Please try again.",
            ),
            500,
        )


@users.route(
    "/update/avatar/<avatarid>", methods=["PUT"]
)
@token_required
def updateProfile(userObj, avatarid):
    print(userObj)
    try:
        link = app.db.avatars.find_one(
            {"id": int(avatarid)}, {"_id": 0}
        )
        app.db.user.update_one(
            {"id": int(userObj["id"])},
            {"$set": {"profile": link["link"]}},
        )
        return jsonify({"success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"success": False}), 500


@users.route("/delete", methods=["DELETE"])
@token_required
def deleteuser(userObj):
    try:
        app.db.user.delete_one(
            {"id": int(userObj.id)}
        )
        return jsonify({"success": True}), 200
    except Exception:
        return (
            jsonify(
                {"success": False, "id": f"{id}"}
            ),
            500,
        )


@users.route("/watched/add", methods=["POST"])
@token_required
def add_to_watched(userObj):
    try:
        req = request.get_json()

        if not req:
            return (
                jsonify(
                    success=False,
                    message="Invalid request",
                ),
                BAD_REQUEST,
            )

        if not (
            "content_id" in req
            and "type" in req
            and "timeStamp" in req
        ):
            return (
                jsonify(
                    success=False,
                    message="Invalid request!",
                ),
                BAD_REQUEST,
            )

        if req["type"] == "tv" and not (
            "season" in req and "episode" in req
        ):
            return (
                jsonify(
                    success=False,
                    message="Invalid request!",
                ),
                BAD_REQUEST,
            )

        already_exists = None
        data = {
            "content_id": req["content_id"],
            "type": req["type"],
            "time": req["timeStamp"],
        }
        match = {
            "content_id": req["content_id"],
            "type": req["type"],
        }

        if req["type"] == "tv":
            data["season"] = req["season"]
            data["episode"] = req["episode"]
            match["season"] = req["season"]
            match["episode"] = req["episode"]

        already_exists = app.db.user.find_one(
            {
                "email": userObj["email"],
                "watched": {"$elemMatch": match},
            }
        )

        if already_exists is None:
            app.db.user.update_one(
                {"email": userObj["email"]},
                {"$push": {"watched": data}},
            )
            return (
                jsonify(
                    success=True,
                    message="Added to watched.",
                ),
                201,
            )

        return (
            jsonify(
                success=False,
                message="Already Exists",
            ),
            CONFLICT,
        )

    except Exception:
        return (
            jsonify(
                success=False,
                message="Something Went Wrong!",
            ),
            500,
        )


@users.route("/watched/fetch", methods=["GET"])
@token_required
def get_watched(userObj):
    try:
        email = userObj["email"]

        user = app.db.user.find_one(
            {"email": email},
            {"_id": 0, "watched": 1, "id": 1},
        )

        if user is None:
            return (
                jsonify(
                    success=True,
                    message="Watched.",
                    results=[],
                    id=user["id"],
                    email=userObj["email"],
                ),
                200,
            )

        return (
            jsonify(
                success=True,
                message="Watched.",
                results=list(
                    reversed(
                        user["watched"][-20:]
                    )
                ),
                id=user["id"],
                email=userObj["email"],
            ),
            200,
        )

    except Exception:
        return (
            jsonify(
                success=False,
                message="Something Went Wrong!",
            ),
            500,
        )
