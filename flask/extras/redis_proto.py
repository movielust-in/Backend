"""
Genrates a txt file containing redis protocol for latest IMDB ratings gathered from IMDB dataset dump.
"""

import json
from urllib.request import urlopen
import pandas as pd

import redis

r = redis.Redis(
    host="redis-13559.c301.ap-south-1-1.ec2.cloud.redislabs.com",
    port=13559,
    password="I1yhozk51qBAFgaPCUzjEJEPqP5eMZ0y",
)


imdb_ratings = None

with urlopen(
    "https://datasets.imdbws.com/title.ratings.tsv.gz"
) as response:
    print("Downloading Imdb ratings in progress")
    imdb_ratings = pd.read_csv(
        response,
        sep="\t",
        compression="gzip",
        header=0,
    )
    print("IMDB rating Loaded")


length = len(imdb_ratings.index)


def gen_redis_proto(cmd, key, value):
    proto = ""

    proto = "*3" + "\r\n"

    # for arg in args1:
    arg = cmd
    proto = proto + "$" + str(len(arg)) + "\r\n"
    proto = proto + arg + "\r\n"

    arg = key
    proto = proto + "$" + str(len(arg)) + "\r\n"
    proto = proto + arg + "\r\n"

    arg = value
    proto = proto + "$" + str(len(arg)) + "\r\n"
    proto = proto + arg + "\r\n"

    return proto


with open(
    "proto.txt", "w", encoding="utf8"
) as file:
    for index, row in imdb_ratings.iterrows():
        valueStr = json.dumps(
            dict(
                rating=row.get("averageRating"),
                votes=row.get("numVotes"),
            )
        )
        movie_id = row.get("tconst")
        protoStr = gen_redis_proto(
            "SET", movie_id, valueStr
        )
        file.write(protoStr)
        print(f"{index}/{length}")
