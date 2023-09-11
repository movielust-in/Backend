from http import HTTPStatus
from os import environ
from urllib.request import urlopen
import pandas as pd
from dotenv import load_dotenv
from flask import Blueprint, jsonify
from imagekitio import ImageKit

from .torrent import torrents as torrent_blueprint
from .admin import adminroutes as admin_blueprint


load_dotenv()

routes = Blueprint("Routes", __name__)

routes.register_blueprint(
    torrent_blueprint, url_prefix="/torrent"
)

routes.register_blueprint(
    admin_blueprint, url_prefix="/admin"
)

imdb_ratings = None

try:
    if environ.get("FLASK_DEBUG") == "production":
        with urlopen(
            "https://datasets.imdbws.com/title.ratings.tsv.gz"
        ) as response:
            print(
                " * Downloading movie ratings from IMDB"
            )
            imdb_ratings = pd.read_csv(
                response,
                sep="\t",
                compression="gzip",
                header=0,
            )
            print("* IMDB ratings Loaded")
    else:
        with open(
            "src/static/data.tsv",
            "r",
            encoding="UTF-8",
        ) as rating_file:
            print(
                " * Loading IMDB ratings from local file."
            )
            imdb_ratings = pd.read_csv(
                rating_file, sep="\t", header=0
            )

except Exception as e:
    print(e)
    print(
        " * Running Server without ratings data."
    )
    imdb_ratings = None


@routes.route(
    "/movie/imdb-rating/<imdb_id>",
    methods=["GET"],
)
def get_imdb_rating(imdb_id):
    try:
        if imdb_ratings is None:
            return (
                jsonify(
                    success=False,
                    message="No ratings",
                ),
                404,
            )

        movie = imdb_ratings.loc[
            imdb_ratings["tconst"] == imdb_id,
            ("averageRating", "numVotes"),
        ].iloc[0]

        if movie is None:
            return (
                jsonify(
                    error=True,
                    message=HTTPStatus.NOT_FOUND.phrase,
                ),
                404,
            )

        rating = movie.get(key="averageRating")

        vote_count = movie.get(key="numVotes")

        return (
            jsonify(
                success=True,
                id=imdb_id,
                rating=rating,
                votes=vote_count,
            ),
            200,
        )

    except Exception:
        return (
            jsonify(
                success=False,
                message="Not found!",
            ),
            404,
        )


@routes.route(
    "/movie/imdb-ratings/<imdb_ids>",
    methods=["GET"],
)
def get_imdb_ratings(imdb_ids):
    try:
        if imdb_ratings is None:
            return (
                jsonify(
                    success=False,
                    message="No ratings",
                ),
                404,
            )

        ratings = []

        for imdb_id in imdb_ids.split(","):
            try:
                rating = imdb_ratings.loc[
                    imdb_ratings["tconst"]
                    == imdb_id,
                    ("averageRating", "numVotes"),
                ].iloc[0]
                ratings.append(
                    {
                        "id": imdb_id,
                        "rating": rating.get(
                            key="averageRating"
                        ),
                        "vote_count": rating.get(
                            key="numVotes"
                        ),
                    }
                )
            except:
                ratings.append(
                    {
                        "id": imdb_id,
                        "rating": 0,
                        "vote_count": 0,
                    }
                )

        return (
            jsonify(
                success=True, results=ratings
            ),
            200,
        )

    except Exception:
        return (
            jsonify(
                success=False,
                message="Not found!",
            ),
            404,
        )


@routes.route("/imagekit/auth", methods=["GET"])
def imagekit_auth():
    imagekit = ImageKit(
        public_key="public_/pYuHcB5K5D2m38lljqgWlbOBe4=",
        private_key="private_uYSzd4ZBX1S2R2fcRe+FTEoEMBo=",
        url_endpoint="https://ik.imagekit.io/movielust",
    )

    auth_params = (
        imagekit.get_authentication_parameters()
    )

    print(auth_params)

    return jsonify(auth_params), 200
