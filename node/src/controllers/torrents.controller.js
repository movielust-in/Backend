import axios from "axios";
import { Movie } from "../models/torrent.model.js";
import * as cheerio from "cheerio";

export const YTSMovieMagnet = async (req, res) => {
  try {
    // console.log("Getting movie torrents");
    const imdb_id = req.params.imdb_id;
    const tmdb_id = req.params.tmdb_id;
    let arr = [];
    let movie_json;

    const check_exist = await Movie.findOne({ id: tmdb_id });

    if (check_exist) {
      return res.send(check_exist.links);
    }

    await axios
      .get(`https://yts.mx/api/v2/movie_details.json?imdb_id=${imdb_id}`)
      .then((res) => {
        movie_json = res.data.data.movie;
        const movie_torrent = movie_json.torrents;
        movie_torrent.map((torrents) => {
          let dict = {
            quality: torrents.quality,
            magnet: torrents.url,
            size: torrents.size,
            size_bytes: torrents.size_bytes,
            hash: torrents.hash,
          };
          arr.push(dict);
        });
      })
      .catch((err) => {
        console.log(err);
      });

    if (arr.length > 0) {
      await Movie.updateOne(
        { id: tmdb_id, name: movie_json.title },
        { $set: { links: arr } }
      );
      return res.send(arr);
    } else {
      return res.send(false);
    }
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const showMagnet = async (req, res) => {
  let show = req.params.show;
  let episode = req.params.episode;
  let season = req.params.season;

  const url = `https://ytstv.me/episode/${show.replaceAll(
    " ",
    "-"
  )}-season-${season}-episode-${episode}`;
};

export const tvMagnet = async (req, res) => {
  try {
    let name = req.params.name;
    let season = req.params.s;
    let episode = req.params.e;
    const titles = [];

    const url = `https://yts-movie.com/${name}-season-${season}-episode-${episode}`;

    await axios.get(url).then((res) => {
      const htmlData = res.data;
      const $ = cheerio.load(htmlData);

      $("div > a").each((_idx, el) => {
        const title = $(el).text();
        titles.push(title);
      });
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
