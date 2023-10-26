from http import HTTPStatus
from os import environ
from urllib.request import urlopen
import pandas as pd
from dotenv import load_dotenv
from flask import Blueprint, jsonify
from imagekitio import ImageKit

from .torrent import torrents as torrent_blueprint

# from .admin import adminroutes as admin_blueprint


load_dotenv()

routes = Blueprint("Routes", __name__)

routes.register_blueprint(
    torrent_blueprint, url_prefix="/torrent"
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
