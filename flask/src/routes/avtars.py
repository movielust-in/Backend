from pymongo import DESCENDING
from flask import (
    Blueprint,
    current_app as app,
    request,
    jsonify,
)

# from app.middlewares.validator import validate
# from app.validation import avtars_validation

avatars = Blueprint("avtars", __name__)


@avatars.route("/", methods=["POST"])
# @validate(avtars_validation.AvtarLink)
def addAvatar():
    with app.app_context():

        try:
            req = request.get_json()
            link = req["link"]
            last_avatar = app.db.avatars.find_one(
                {}, sort=[("_id", DESCENDING)]
            )
            app.db.avatars.insert_one(
                {
                    "id": int(last_avatar["id"])
                    + 1,
                    "link": link,
                }
            )
            return jsonify({"success": True}), 200
        except Exception:
            return (
                jsonify({"success": False}),
                500,
            )


@avatars.route("/getall", methods=["GET"])
def getAvatar():
    try:
        Avatars = app.db.avatars.find(
            {}, {"_id": 0}
        )
        # print(list(Avatars))
        return (
            jsonify(
                {
                    "success": True,
                    "avtars": list(Avatars),
                }
            ),
            200,
        )
    except Exception:
        return jsonify({"success": False}), 500


@avatars.route("/<avatarid>", methods=["DELETE"])
def deleteAvatar(avatarid):
    try:
        app.db.avatars.delete_one(
            {"id": int(avatarid)}
        )
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Avatar Removed.",
                }
            ),
            204,
        )
    except:
        return jsonify({"success": False}), 500
