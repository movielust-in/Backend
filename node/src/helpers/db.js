import { connect, set } from 'mongoose';

export const connectDB = async () =>

    new Promise((resolve) => {
        (async () => {
            try {
                set("strictQuery", false);
                await connect(process.env.DATABASE_URL);
                console.log("Database connected.");
                resolve();
            } catch (err) {
                console.log("Database error.", err);
                throw new Error(err);
            }
        })();
    })

