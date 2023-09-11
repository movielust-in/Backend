import { AvatarModel, UserModel } from "../models/user.model.js";
import { Movie, TV } from "../models/torrent.model.js";

export const getAvatars = async (req, res) => {
  try {
    // console.log("Admin is getting Avatar data");
    let avatars = await AvatarModel.find();
    const data = {
      avtars: avatars,
    };
    res.send(data);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

export const getAllUsers = async (req, res) => {
  try {
    // console.log("Admin is getting User data");
    const projection = {
      _id: 0,
      password: 0,
      watched: 0,
      watchlist: 0,
      visits: 0,
      logins: 0,
    };
    let User = await UserModel.find({}, projection);
    const data = {
      results: User,
    };
    res.send(data);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const getAllMovies = async (req, res) => {
  try {
    // console.log("Admin is getting movie data");

    let Movies = await Movie.find({}, { _id: 0 });
    const data = {
      results: Movies,
    };
    res.send(data);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const addMovie = async (req, res) => {
  try {
    // console.log("Admin is adding movie ");

    let movie_data = req.body;
    const check_exists = await Movie.findOne({ id: movie_data.id });
    if (check_exists) {
      return res.send("Already exists");
    } else {
      await Movie.updateOne(movie_data);
      return res.send(true);
    }
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const deleteMovie = async (req, res) => {
  try {
    // console.log("Admin is delete movie data");

    let movieID = req.params.id;
    const check_exists = await Movie.findOne({ id: movieID });
    if (check_exists) {
      await Movie.deleteOne({ id: movieID });
      return res.send(true);
    } else {
      return res.send(false);
    }
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const getAllTV = async (req, res) => {
  try {
    // console.log("Admin is fetching tv data");
    let Tv_links = await TV.find({}, { _id: 0 });
    const data = {
      results: Tv_links,
    };
    res.send(data);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const deleteTV = async (req, res) => {
  try {
    let TVID = req.params.id;
    const check_exists = await TV.findOne({ id: TVID });
    if (check_exists) {
      await TV.deleteOne({ id: TVID });
      return res.send(true);
    } else {
      return res.send(false);
    }
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const uptime = async (req, res) => {
  return res.send("nothing");
};