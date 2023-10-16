import dotenv from 'dotenv';

import app from './app.js';
import { connectDB } from './helpers/database.js';
import { verifyTransport } from './helpers/nodemailer.js';

dotenv.config();

await connectDB();

await verifyTransport();

const PORT = process.env.PORT || 3001;

const server = app.listen(PORT, () => {
    console.log('Listening at', PORT);
});

const exitHandler = () => {
    // eslint-disable-next-line unicorn/no-process-exit
    if (!server) return process.exit();

    server.close(() => {
        console.log('Server closed.');
        // eslint-disable-next-line unicorn/no-process-exit
        process.exit();
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
