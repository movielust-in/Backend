import cors from "cors";
import morgan from "morgan";
import helmet from "helmet";
import express, { json } from "express";

import mainRouter from "./routes/routes.js";
import flaskProxy from "./middlewares/flask-proxy.middleware.js";

const app = express();

app.use(json());
app.use(helmet());
app.use(cors());
app.use(express.static("public"));
app.use(morgan(process.env.NODE_ENV != "production" ? "dev" : "combined"));

app.use(mainRouter);

app.use("/flask", flaskProxy);

app.use("/", (req, res) => {
  res.status(200).send({ status: "Server is running" });
});

export default app;
