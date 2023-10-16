import { connect, set } from 'mongoose';

export const connectDB = async () =>
    new Promise((resolve) => {
        (async () => {
            try {
                set('strictQuery', false);
                await connect(process.env.DATABASE_URL);
                console.log('Database connected.');
                resolve();
            } catch (error) {
                console.log('Database error.', error);
                throw new Error(error);
            }
        })();
    });
