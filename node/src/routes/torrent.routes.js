import { Router } from 'express';
import { YTSMovieMagnet } from '../controllers/torrents.controller.js';

// eslint-disable-next-line new-cap
const torrentRouter = Router();

torrentRouter.get('/movie/yts/:imdb_id/:tmdb_id', YTSMovieMagnet);

export default torrentRouter;
