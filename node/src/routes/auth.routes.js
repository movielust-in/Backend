import { Router } from 'express';
import {
    userLogin,
    sendOtp,
    verifyOTP,
    createAccount,
    resetpassword,
    adminLogin,
} from '../controllers/auth.controller.js';

// eslint-disable-next-line new-cap
const authRouter = Router();

authRouter.post('/login', userLogin);
authRouter.post('/admin/login', adminLogin);

authRouter.post('/sendotp', sendOtp);

authRouter.post('/verifyotp', verifyOTP);

authRouter.post('/signup', createAccount);
authRouter.post('/resetpassword', resetpassword);

export default authRouter;
