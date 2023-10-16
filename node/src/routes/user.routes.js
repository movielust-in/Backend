import { Router } from "express";
import {
  getWatched,
  addWatched,
  getUserProfile,
  updateAvatar,
  deleteuser,
  getWatchlist,
  addToWatchlist,
  removeWatchlist,
  deleteWatched,
} from "../controllers/user.controller.js";

import authMiddleware from "../middlewares/auth.middleware.js";

// eslint-disable-next-line new-cap
const userRouter = Router();

userRouter.use(authMiddleware);

userRouter.get("/watched", getWatched);
userRouter.post("/addWatched", addWatched);
userRouter.post("/deleteWatched", deleteWatched);

userRouter.get("/watchlist/get", getWatchlist);
userRouter.post("/watchlist/add", addToWatchlist);
userRouter.delete("/watchlist/remove", removeWatchlist);

userRouter.get("/delete", deleteuser);

userRouter.get("/profile", getUserProfile);
userRouter.put("/update/avatar", updateAvatar);

export default userRouter;
