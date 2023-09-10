from flask import Blueprint
from .movies import movie_torrents
from .shows import show_torrents

torrents = Blueprint("Torrents", __name__)

torrents.register_blueprint(
    movie_torrents, url_prefix="/movie"
)
torrents.register_blueprint(
    show_torrents, url_prefix="/show"
)


@torrents.after_request
def add_header(response):
    if "Cache-Control" not in response.headers:
        response.headers[
            "Cache-Control"
        ] = "max-age=31536000"
    return response
