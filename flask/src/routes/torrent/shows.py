from concurrent.futures import ThreadPoolExecutor
import itertools
from bs4 import BeautifulSoup
import requests
from flask import (
    Blueprint,
    current_app as app,
    jsonify,
)

show_torrents = Blueprint(
    "Show torrents", __name__
)


def get_episode_magnet(episode, season, show):
    try:
        link = f"https://ytstv.me/episode/{str(show).replace(' ','-')}-season-{str(season)}-episode-{str(episode)}"
        res = requests.get(link)
        if res.status_code != 200:
            return []
        soup = BeautifulSoup(res.content, "lxml")

        divs = soup.findAll(
            "div",
            attrs={
                "class": "btn-group btn-group-justified embed-selector"
            },
        )

        links = [
            div for div in divs[1] if div != "\n"
        ]

        torrent = list()
        for link in links:
            torrent_type = ""
            href = link["href"]
            if href:
                if "magnet:?" in href:
                    torrent_type = "magnet"
                else:
                    torrent_type = "torrent"
                span = link.findAll("span")
                language = str(span[2].text)

                try:
                    quality = str(
                        span[4].text
                    ).split(".", 1)[1]
                except IndexError:
                    try:
                        quality = str(
                            span[4].text
                        ).split(")", 1)[1]
                    except IndexError:
                        quality = str(
                            span[4].text
                        ).split(")", 1)[0]

                obj = {
                    "season": season,
                    "quality": quality,
                    "episode": episode,
                    "lang": language,
                }
                if torrent_type == "torrent":
                    obj["type"] = "torrent"
                    obj["torrent"] = href
                else:
                    obj["type"] = "magnet"
                    obj["magnet"] = href

                torrent.append(obj)

        return torrent

    except Exception:

        return []


# returns magnets/torrents for all episodes of provided season of a show
@show_torrents.route(
    "/<tmdb_id>/<show>/<season>/<total_episodes>",
    methods=["GET"],
)
def getMagnet(
    tmdb_id, show, season, total_episodes
):
    try:
        try:
            if app.db.tv_links is not None:
                exists = app.db.tv_links.find_one(
                    {
                        "id": tmdb_id,
                        "title": show,
                        "seasons": {
                            "$elemMatch": {
                                "season": season
                            }
                        },
                    },
                    {
                        "_id": 0,
                        "seasons": {
                            "$elemMatch": {
                                "season": season
                            }
                        },
                    },
                )

                if exists:
                    return (
                        jsonify(
                            success=True,
                            message="Done",
                            source="DB",
                            results=exists[
                                "seasons"
                            ][0]["links"],
                        ),
                        200,
                    )
                raise Exception("Not in DB!")
        except Exception:

            if not (
                season.isdigit()
                and total_episodes.isdigit()
                and int(total_episodes) > 0
            ):
                return (
                    jsonify(
                        success=False,
                        message="Invalid request!",
                    ),
                    400,
                )

            total_episodes = int(total_episodes)
            # try:
            with ThreadPoolExecutor(
                max_workers=10
            ) as pool:
                responses = list(
                    pool.map(
                        get_episode_magnet,
                        list(
                            range(
                                1,
                                total_episodes
                                + 1,
                            )
                        ),
                        itertools.repeat(
                            season,
                            total_episodes + 1,
                        ),
                        itertools.repeat(
                            show,
                            total_episodes + 1,
                        ),
                    )
                )

            responses = [
                response
                for response in responses
                if response is not None
            ]

            if len(responses) > 0:
                try:
                    app.db.tv_links.update_one(
                        {
                            "id": tmdb_id,
                            "title": show,
                        },
                        {
                            "$push": {
                                "seasons": {
                                    "season": season,
                                    "links": responses,
                                }
                            }
                        },
                        upsert=True,
                    )
                except Exception as e:
                    print(e)

            if len(responses):
                return (
                    jsonify(
                        success=True,
                        message="Done",
                        source="YTSTV",
                        results=responses,
                    ),
                    200,
                )
            return (
                jsonify(
                    success=False,
                    message="No data Available",
                ),
                404,
            )
    except Exception as e:
        print(e)
        return (
            jsonify(
                success=False, message="Faileld"
            ),
            500,
        )


@show_torrents.route(
    "/tv/magnet/full-season/<id>/<name>/<season>"
)
def full_season_magnets(showid, name, season):

    try:

        exists = app.db.tv_links.find_one(
            {
                "id": showid,
                "title": name,
                "complete": {
                    "$elemMatch": {
                        "season": season
                    }
                },
            },
            {
                "_id": 0,
                "complete": {
                    "$elemMatch": {
                        "season": season
                    }
                },
            },
        )

        if exists is not None:
            return jsonify(
                success=True,
                message="Done",
                results=exists["complete"][0][
                    "links"
                ],
                source="DB",
            )

        ytstv = None

        try:
            ytstv = requests.get(
                f"https://ytstv.me/episode/{name.lower().replace(' ','-')}-season-{season}-complete"
            )
            if ytstv.status_code == 404:
                raise Exception
        except:
            ytstv = requests.get(
                f"https://ytstv.me/episode/{name.lower().replace(' ','-')}-season-{season}-full-episodes"
            )

        if ytstv.status_code == 404:
            return (
                jsonify(
                    success=False,
                    message="No data for series",
                ),
                404,
            )

        soup = BeautifulSoup(
            ytstv.content, "lxml"
        )
        links = soup.findAll(
            "a", attrs={"class": "lnk-lnk"}
        )

        torrent = []

        for link in links:
            href = str(link["href"])
            torrent_type = None
            quality = ""
            if "magnet:?" in href:
                torrent_type = "magnet"
            elif ".torrent" in href:
                torrent_type = "torrent"
            if torrent_type:
                span = link.findAll("span")
                language = str(span[1].text)
                try:
                    quality = str(
                        span[2].text
                    ).split(".", 1)[1]
                except IndexError:
                    try:
                        quality = str(
                            span[2].text
                        ).split(")", 1)[1]
                    except IndexError:
                        quality = str(
                            span[2].text
                        ).split(")", 1)[0]
                torrent.append(
                    {
                        "quality": quality,
                        torrent_type: href,
                        "lang": language,
                        "type": torrent_type,
                    }
                )

        if not exists:
            app.db.tv_links.update_one(
                {"id": showid, "title": name},
                {
                    "$push": {
                        "complete": {
                            "season": season,
                            "links": torrent,
                        }
                    }
                },
                upsert=True,
            )

        return (
            jsonify(
                success=True,
                message="Done",
                results=torrent,
                source="YTSTV",
            ),
            200,
        )
    except Exception:

        return (
            jsonify(
                error=True,
                Success=False,
                message="Something Went Wrong! Please try again.",
            ),
            500,
        )
