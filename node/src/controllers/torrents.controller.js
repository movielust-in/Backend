import axios from 'axios';
import { Movie } from '../models/torrent.model.js';
import { magnetFromHash } from '../helpers/magnetFromHash.js';

export const YTSMovieMagnet = async (req, res) => {
    try {
        // console.log("Getting movie torrents");
        const imdb_id = req.params.imdb_id;
        const tmdb_id = req.params.tmdb_id;

        const check_exist = await Movie.findOne({ id: tmdb_id });

        if (check_exist) {
            return res.send(check_exist.links);
        }

        const ytsRes = await axios.get(
            `https://yts.mx/api/v2/movie_details.json?imdb_id=${imdb_id}`
        );

        const movieData = ytsRes.data.data.movie;
        const movieTorrents = movieData.torrents;
        const mangets = movieTorrents.map((torrent) => {
            return {
                quality: torrent.quality,
                magnet: magnetFromHash(
                    torrent.hash,
                    movieData.title,
                    torrent.quality
                ),
                size: torrent.size,
                size_bytes: torrent.size_bytes,
                hash: torrent.hash,
            };
        });

        if (mangets.length <= 0) {
            return res.status(404).send(false);
        }

        await Movie.updateOne(
            { id: tmdb_id, name: movieData.title },
            { $set: { links: mangets } }
        );

        return res.send(mangets);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
};
