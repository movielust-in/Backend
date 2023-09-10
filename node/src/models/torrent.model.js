import pkg from "mongoose";

const { Schema, model } = pkg;

const MovieSchema = new Schema({
  id: {
    type: String,
  },
  name: {
    type: String,
  },
  links: {
    type: Array,
  },
});

const Movie = model("movielinks", MovieSchema, "movie_links");

const TVSchema = new Schema({
  id: {
    type: String,
  },
  title: {
    type: String,
  },
  seasons: {
    type: Array,
  },
});

const TV = model("tvlinks", TVSchema, "tv_links");

export { Movie, TV };
