import cors from "cors";
import morgan from "morgan";
import helmet from "helmet";
import dotenv from "dotenv";
import express, { json } from "express";

import { verifyTransport } from "./helpers/nodemailer.js";
import mainRouter from "./routes/routes.js";
import flaskProxy from "./middlewares/flask-proxy.middleware.js";
import { connectDB } from "./helpers/db.js";

dotenv.config();

const PORT = process.env.PORT || 3001;

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

await connectDB();

await verifyTransport();


app
  .listen(PORT, () => {
    console.log("Server is running on port:", PORT);
  })
  .on("err", (err) => {
    console.log("Server error.", err);
  });
