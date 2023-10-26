import { createGunzip } from "node:zlib";
import { Readable } from "node:stream";
import { finished } from "node:stream/promises";
import {
  connect as connectDatabase,
  disconnect as closeDatabaseConnection,
} from "mongoose";
import { parse } from "csv";

import { imdbRating } from "./models/imdb-rating.model.js";

const startTime = Date.now();
const RATING_DATASET_URL = "https://datasets.imdbws.com/title.ratings.tsv.gz";
const ratings = [];

console.log("🚀 Connecting to databse....");

await connectDatabase(process.env.DB_URL);

console.log("✅ Connected to databse.");

const gunZip = createGunzip();

const tsvParser = parse({ delimiter: "\t" });

console.log("🚀 Fetching IMDB Rating Dataset...");

const res = await fetch(RATING_DATASET_URL);

console.log("✅ Completed: Fetching IMDB Rating Dataset.");

console.log("🚀 Processing Data...");

await finished(
  Readable.fromWeb(res.body).pipe(gunZip).pipe(tsvParser).on("data", addRecord)
);

ratings.shift();

console.log("✅ Completed: Processing Data.");

console.log("🚀 Deleting previous ratings in database....");

await imdbRating.deleteMany({});

console.log("✅ Completed: Deleting previous ratings in database.");

console.log("🚀 Inserting new ratings in database....");

await imdbRating.insertMany(ratings, { lean: true, limit: null });

console.log("✅ Completed: Inseting new ratings in database.");

closeDatabaseConnection();

const timeDelta = Date.now() - startTime;

console.log(
  `🔥 Job completed in ${millisToMinutesAndSeconds(timeDelta)} seconds.`
);

function addRecord(data) {
  ratings.push({ imdb_id: data[0], rating: data[1], vote_count: data[2] });
}

function millisToMinutesAndSeconds(millis) {
  const minutes = Math.floor(millis / 60_000);
  const seconds = ((millis % 60_000) / 1000).toFixed(0);
  return `${minutes ? minutes + " Minutes, " : ""}${
    seconds < 10 ? "0" : ""
  }${seconds} Seconds`;
}
