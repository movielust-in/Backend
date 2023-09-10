import https from "https";
import zlib from "zlib";
import { parse } from "csv";
import { AvatarModel } from "../models/user.model.js";
var ratings = {};

export const getAllAvatar = async (req, res) => {
  try {
    const link = await AvatarModel.find({}, { _id: 0 });
    res.send(link);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

// ---------------------------------------- IMDB Rating -----------------------------------------------

https.get(
  "https://datasets.imdbws.com/title.ratings.tsv.gz",
  function (response) {
    const unzip = zlib.createGunzip();

    const tsv = parse({
      delimiter: "/t",
    });

    let addRecord = (data) => {
      const rating = data[0].split("\t");
      ratings[rating[0]] = { rating: rating[1], count: rating[2] };
    };
    response.pipe(unzip).pipe(tsv).on("data", addRecord);
  }
);

export const imdbRating = async (req, res) => {
  try {
    // console.log("IMDB rating");

    if (Object.keys(ratings).length === 0) {
      res.status(500).json({ message: "No ratings" });
    }
    let movie_id = req.params.id;

    const content_rating = ratings[movie_id];

    if (content_rating == undefined) {
      return res.send(false);
    }

    let movieRating = {
      id: movie_id,
      rating: content_rating.rating,
      votes: content_rating.count,
    };

    res.send({ movieRating });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
//n

export const imdbRatings = async (req, res) => {
  try {

    if (Object.keys(ratings).length === 0) {
      res.status(500).json({ message: "No ratings" });
    }
    let movie_ids = req.params.id;
    const arr = movie_ids.split(",");

    let movieRating;
    let allRating = [];
    for (let i = 0; i < arr.length; i++) {
      const rating = arr[i];
      movieRating = {
        id: arr[i],
        rating: rating.rating,
        votes: rating.count,
      };

      allRating.push(movieRating);
    }
    res.send(allRating);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
