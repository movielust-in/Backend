import { Router } from "express";
import {
  addMovie,
  deleteMovie,
  deleteTV,
  getAllMovies,
  getAllTV,
  getAllUsers,
  getAvatars,
} from "../controllers/admin.controller.js";

const adminRouter = Router();

adminRouter.get("/avatar/getall", getAvatars);
adminRouter.get("/user/all", getAllUsers);
adminRouter.get("/movies/all", getAllMovies);
adminRouter.get("/tv/all", getAllTV);
adminRouter.post("/movie/insert", addMovie);
adminRouter.delete("/movie/delete/:id", deleteMovie);
adminRouter.delete("/tv/delete/:id", deleteTV);

export default adminRouter;
