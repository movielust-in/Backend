import { Router } from "express";
import {
  showMagnet,
  tvMagnet,
  YTSMovieMagnet,
} from "../controllers/torrents.controller.js";

const torrentRouter = Router();

torrentRouter.get("/movie/yts/:imdb_id/:tmdb_id", YTSMovieMagnet);
torrentRouter.get("/tv/show/:id/:showname/:season/:totalepi", showMagnet);
torrentRouter.get("/tv/:name/:s/:e", tvMagnet);

export default torrentRouter;
