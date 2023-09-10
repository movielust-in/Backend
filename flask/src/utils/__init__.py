import math
from os import environ
import random
from datetime import datetime, timezone
import pytz
import requests
from flask import current_app as app
from src.utils import constants

TMDB_KEY = environ.get("TMDB_KEY")


def get_detail(movieid):
    url = "https://api.themoviedb.org/3/movie/{id}?api_key={key}&language=en-US".format(
        id=movieid, key=TMDB_KEY
    )
    return requests.get(url)


def get_similar_tmdb(
    content_type, content_id, page
):
    url = "https://api.themoviedb.org/3/{type}/{id}/similar?api_key={key}&language=en-US&page={page}".format(
        type=content_type,
        id=content_id,
        page=page,
        key=TMDB_KEY,
    )
    return requests.get(url)


def get_movie_details(contenttype, movieid):
    url = "https://api.themoviedb.org/3/{type}/{movie_id}?api_key={key}&language=en-US".format(
        type=contenttype,
        movie_id=movieid,
        key=TMDB_KEY,
    )
    return requests.get(url).json()


def gen_otp():
    digits = [i for i in range(0, 10)]
    otp = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        otp += str(digits[index])
    return otp


def verify_otp(email, otp, otp_type):
    try:
        if len(otp) != 6 or (not otp.isdecimal()):
            return False
        otp_in_db = app.db.otp.find_one(
            {
                "email": email,
                "otp": otp,
                "type": constants.OTP_TYPES[
                    otp_type
                ],
            }
        )
        if otp_in_db is None:
            return False
        isExpired = datetime.now(
            timezone.utc
        ) > otp_in_db["exp"].replace(
            tzinfo=pytz.UTC
        )
        if isExpired:
            return False
        return True
    except Exception:
        return 0
