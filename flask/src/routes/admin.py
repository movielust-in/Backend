from flask import (
    current_app as app,
    Blueprint,
    jsonify,
    redirect,
    request,
)
from jwt import decode, InvalidTokenError
from os import environ

adminroutes = Blueprint("Admin routes", __name__)


@adminroutes.before_request
def admin_before_req():
    if request.method != "OPTIONS":
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
            decode(
                token,
                environ.get("ADMIN_SECRET"),
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


@adminroutes.route("/user/all", methods=["GET"])
def get_all_user():
    try:
        users = app.db.user.find(
            {},
            {
                "_id": 0,
                "password": 0,
                "watched": 0,
                "watchlist": 0,
                "visits": 0,
                "logins": 0,
            },
        ).sort("id")
        return (
            jsonify(
                success=True, results=list(users)
            ),
            200,
        )
    except:
        return (
            jsonify(
                error=True,
                success=False,
                message="Something Went Wrong",
            ),
            500,
        )


# returns all movies(magnets/torrents) stored in DB
@adminroutes.route("/movies/all", methods=["GET"])
def get_all_movies():
    try:
        movies = app.db.movie_links.find(
            {}, {"_id": 0}
        )
        return (
            jsonify(
                success=True, results=list(movies)
            ),
            200,
        )
    except:
        return (
            jsonify(
                error=True,
                success=False,
                message="Something Went Wrong",
            ),
            500,
        )


@adminroutes.route("/tv/all", methods=["GET"])
def get_all_tv():
    try:
        tv = app.db.tv_links.find({}, {"_id": 0})
        return (
            jsonify(
                success=True, results=list(tv)
            ),
            200,
        )
    except:
        return (
            jsonify(
                error=True,
                success=False,
                message="Something Went Wrong",
            ),
            500,
        )


@adminroutes.route(
    "/movie/insert", methods=["POST"]
)
def insert_movie():
    try:
        req = request.get_json()
        if not req:
            return (
                jsonify(
                    error=True,
                    success=False,
                    message="Bad request!",
                ),
                400,
            )
        if not (
            "id" in req
            and "name" in req
            and "links" in req
        ):
            return (
                jsonify(
                    error=True,
                    success=False,
                    message="Bad request!",
                ),
                400,
            )

        # movie_links.find_one({"id":req['id'],"name"=req['name'],"links":req['links']})
        exists = app.db.movie_links.find_one(
            {"id": req["id"]}
        )
        if exists:
            return (
                jsonify(
                    success=False,
                    message="Movied Found in DB",
                ),
                302,
            )
        app.db.movie_links.insert_one(req)
        return (
            jsonify(success=True, message="Done"),
            200,
        )
    except Exception:
        return (
            jsonify(
                error=True,
                success=False,
                message="Something Went Wrong!",
            ),
            500,
        )


@adminroutes.route(
    "/movie/delete/<id>", methods=["DELETE"]
)
def delete_movie(movieid):
    try:
        exists = app.db.movie_links.find_one(
            {"id": movieid}
        )
        if exists is None:
            return (
                jsonify(
                    error=True,
                    success=False,
                    message="Does not exist!",
                ),
                404,
            )
        app.db.movie_links.delete_one(
            {"id": movieid}
        )
        return (
            jsonify(
                success=True, message="Deleted"
            ),
            204,
        )
    except Exception:
        return (
            jsonify(
                error=True,
                success=False,
                message="Something Went Wrong! Please try again.",
            ),
            500,
        )


@adminroutes.route(
    "/tv/delete/<id>", methods=["DELETE"]
)
def delete_tv(showid):
    try:
        exists = app.db.tv_links.find_one(
            {"id": showid}
        )
        if exists is None:
            return (
                jsonify(
                    error=True,
                    success=False,
                    message="Does not exist!",
                ),
                404,
            )
        app.db.tv_links.delete_one({"id": showid})
        return (
            jsonify(
                success=True, message="Deleted"
            ),
            204,
        )
    except Exception:
        return (
            jsonify(
                error=True,
                success=False,
                message="Something Went Wrong! Please try again.",
            ),
            500,
        )


@adminroutes.route("/uptime")
def uptime():
    return redirect(
        "https://stats.uptimerobot.com/ZDREBs73Rr",
        code=302,
    )
