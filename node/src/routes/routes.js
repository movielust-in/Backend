import { Router } from "express";
import userRouter from "./user.routes.js";
import authRouter from "./auth.routes.js";
import adminRouter from "./admin.routes.js";
import torrentRouter from "./torrent.routes.js";

import {
  getAllAvatar,
  imdbRating,
  imdbRatings,
} from "../controllers/main.controller.js";

const mainRouter = Router();

mainRouter.use("/admin", adminRouter);
mainRouter.use("/user", userRouter);
mainRouter.use("/auth", authRouter);
mainRouter.use("/torrent", torrentRouter);

mainRouter.get("/avatar/getall", getAllAvatar);
mainRouter.get("/movie/imdb-rating/:id", imdbRating);
mainRouter.get("/movie/imdb-ratings/:id", imdbRatings);

export default mainRouter;
