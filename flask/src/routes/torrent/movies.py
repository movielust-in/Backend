import requests
from bs4 import BeautifulSoup
from flask import (
    current_app as app,
    Blueprint,
    jsonify,
)

movie_torrents = Blueprint(
    "movie torrents", __name__
)


@movie_torrents.route(
    "/<movie_id>/<movie_name>", methods=["GET"]
)
def get_magnet(movie_id, movie_name):
    try:
        exist = app.db.movie_links.find_one(
            {"id": movie_id}
        )
        if exist is not None:
            return jsonify(
                success=True,
                results=exist["links"],
                source="DB",
            )
        raise Exception("as")
    except:

        try:
            URL = f"https://yts.mx/movies/{movie_name}"

            res = requests.get(URL)

            if res.status_code != 200:
                return jsonify(success=False), 404

            soup = BeautifulSoup(
                res.content, "lxml"
            )

            links = soup.findAll(
                "div",
                attrs={"class": "modal-torrent"},
            )
            magnets = []

            for link in links:
                a = link.findAll("a")
                p = link.findAll("p")
                title = str(a[0]["title"])
                if "720" in title:
                    magnets.append(
                        {
                            "magnet": a[1][
                                "href"
                            ],
                            "size": str(
                                p[2].string
                            ),
                            "quality": "720p",
                        }
                    )
                elif "1080" in title:
                    magnets.append(
                        {
                            "magnet": a[1][
                                "href"
                            ],
                            "size": str(
                                p[2].string
                            ),
                            "quality": "1080p",
                        }
                    )
            try:
                if len(magnets) > 0:
                    app.db.movie_links.update_one(
                        {
                            "id": movie_id,
                            "name": movie_name,
                        },
                        {
                            "$set": {
                                "links": magnets
                            }
                        },
                        upsert=True,
                    )
            except:
                print(
                    "Error adding movie magnets in DB"
                )

            return (
                jsonify(
                    success=True,
                    results=magnets,
                    source="YTS",
                ),
                200,
            )
        except:
            return (
                jsonify(
                    error=True, success=False
                ),
                500,
            )


# @movie_torrents.route("/<imdb_id>/<tmdb_id>/<movie_name>")
# def get_movie_magnet(imdb_id, tmdb_id, movie_name):
#     try:
#         # exist = app.db.movie_links.find_one({"id": tmdb_id})
#         # if exist is not None:
#         #     return jsonify(success=True, results=exist["links"], source="DB")
#         YTS_API = f"https://yts.mx/api/v2/movie_details.json?imdb_id={imdb_id}"
#         res = requests.get(YTS_API)
#         jsonRes = res.json()
#         print(jsonRes)
#         torrents = jsonRes["data"]["movie"]["torrents"]

#         return jsonify(success=True, results=torrents, source="YTS Api"), 200
#     except Exception as e:
#         print(e)
#         return jsonify(error=True, success=False), 500


# Get bollywood and south
@movie_torrents.route(
    "/hindi/<id>/<movie_name>", methods=["GET"]
)
def get_indiamagnet(movie_id, movie_name):
    try:
        exist = app.db.movie_links.find_one(
            {"id": movie_id}
        )
        if exist is not None:
            return jsonify(
                success=True,
                results=exist["links"],
                source="DB",
            )
        raise Exception("as")
    except:

        try:
            URL = f"https://yts-movie.com/{movie_name}"

            res = requests.get(URL)

            if res.status_code != 200:
                return jsonify(success=False), 404

            soup = BeautifulSoup(
                res.content, "lxml"
            )

            links = soup.findAll(
                "div",
                attrs={
                    "class": "btn-group btn-group-justified embed-selector"
                },
            )[1]

            links = links.findAll("a")
            magnet = []

            for link in links:
                torrent = link["href"]
                spans = link.findAll("span")
                lang = (
                    spans[2]
                    .findAll("span")[0]
                    .text
                )
                quality = spans[4].text

                magnet.append(
                    {
                        "torrent": torrent,
                        "quality": quality,
                        "language": lang,
                    }
                )

            return (
                jsonify(
                    success=True,
                    source="YTS",
                    magnets=magnet,
                ),
                200,
            )
        except Exception:

            return (
                jsonify(
                    error=True, success=False
                ),
                500,
            )


@movie_torrents.route(
    "/yts/<imdb_id>/<tmdb_id>", methods=["GET"]
)
def yts_api_torrent(imdb_id, tmdb_id):
    try:

        exists = app.db.movie_links.find_one(
            {"id": tmdb_id}
        )

        if exists is not None:
            return jsonify(
                success=True,
                results=exists["links"],
                source="DB",
            )

        apiUrl = f"https://yts.mx/api/v2/movie_details.json?imdb_id={imdb_id}"

        res = requests.get(apiUrl)

        if res.status_code != 200:
            return jsonify(success=False), 404

        json = res.json()

        magnets = []

        for torrent in json["data"]["movie"][
            "torrents"
        ]:
            magnets.append(
                {
                    "quality": torrent["quality"],
                    "magnet": torrent["url"],
                    "size": torrent["size"],
                    "size_bytes": torrent[
                        "size_bytes"
                    ],
                    "hash": torrent["hash"],
                }
            )

        try:
            if len(magnets) > 0:
                app.db.movie_links.update_one(
                    {
                        "id": tmdb_id,
                        "name": json["data"][
                            "movie"
                        ]["title"],
                    },
                    {"$set": {"links": magnets}},
                    upsert=True,
                )
        except:
            print(
                "Error adding movie magnets in DB"
            )

        return (
            jsonify(
                success=True,
                results=magnets,
                source="YTS API",
            ),
            200,
        )
    except:
        return (
            jsonify(
                success=False,
                message="Something went wrong!",
            ),
            500,
        )
