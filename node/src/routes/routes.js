import { Router } from 'express';
import userRouter from './user.routes.js';
import authRouter from './auth.routes.js';
import adminRouter from './admin.routes.js';
import torrentRouter from './torrent.routes.js';

import { getAllAvatar } from '../controllers/main.controller.js';

// eslint-disable-next-line new-cap
const mainRouter = Router();

mainRouter.use('/admin', adminRouter);
mainRouter.use('/user', userRouter);
mainRouter.use('/auth', authRouter);
mainRouter.use('/torrent', torrentRouter);

mainRouter.get('/avatar/getall', getAllAvatar);

export default mainRouter;
