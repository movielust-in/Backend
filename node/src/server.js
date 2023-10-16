import dotenv from 'dotenv';

import app from './app.js';
import { connectDB } from './helpers/db.js';
import { verifyTransport } from './helpers/nodemailer.js';

dotenv.config();

await connectDB();

await verifyTransport();

const PORT = process.env.PORT || 3001;

const server = app.listen(PORT, () => {
    console.log('Listening at', PORT);
});

const exitHandler = () => {
    if (!server) return process.exit(1);

    server.close(() => {
        console.log('Server closed.');
        process.exit(1);
    });
};

const unexpectedErrorHandler = (error) => {
    console.error(error);
    exitHandler();
};

process.on('uncaughtException', unexpectedErrorHandler);
process.on('unhandledRejection', unexpectedErrorHandler);

process.on('SIGTERM', () => {
    console.log('SIGTERM RECIEVED.');
    if (server) server.close();
});
