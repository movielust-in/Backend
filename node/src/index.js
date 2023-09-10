import cors from "cors";
import morgan from "morgan";
import helmet from "helmet";
import dotenv from "dotenv";
import express, { json } from "express";
import { connect, set as mongooseSet } from "mongoose";

import { transporter } from "./utils/nodemailer.js";
import mainRouter from "./routes/routes.js";
import flaskProxy from "./middlewares/flask-proxy.middleware.js";

const PORT = process.env.PORT || 3001;

dotenv.config();

const app = express();

app.use(json());
app.use(helmet());
app.use(cors());
app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(json());
app.use(morgan(process.env.ENV != "production" ? "dev" : "combined"));

app.use(mainRouter);

app.use("/flask", flaskProxy);

app.use("/", (req, res) => {
  res.status(200).send({ success: "Server is running" });
});

try {
  mongooseSet("strictQuery", false);
  await connect(process.env.DATABASE_URL);
  console.log("Database connected.");
} catch (err) {
  console.log("Database error.", err);
  throw new Error(err);
}

try {
  await transporter.verify();
  console.log("Mail server verified.");
} catch (err) {
  console.log("Mail server error:", err);
  throw new Error(err);
}

app
  .listen(PORT, () => {
    console.log("Server is running on port:", PORT);
  })
  .on("err", (err) => {
    console.log("Server error.", err);
  });
