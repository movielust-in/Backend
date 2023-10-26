import { Schema, model } from 'mongoose';

const ImdbRatingSchema = new Schema({
    imdb_id: { type: String, index: true },
    rating: Number,
    vote_count: Number,
});

export const imdbRating = model(
    'IMDBRatings',
    ImdbRatingSchema,
    'IMDB_Ratings'
);
