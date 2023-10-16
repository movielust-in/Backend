import jwt from "jsonwebtoken";
import handlebars from "handlebars";
import bcrypt from "bcryptjs";
import { promises as fs } from "node:fs";

import Otp from "../models/auth.model.js";
import { UserModel } from "../models/user.model.js";
import AdminSchema from "../models/admin.model.js";
import { sendMail } from "../utils/nodemailer.js";

// ------------------------------ Send OTP to verify Email  ---------------------------------------------

export const sendOtp = async (req, res) => {
  try {
    const user_credentials = req.body;
    const user_email = user_credentials.email;
    const user_name = user_credentials.name;
    const user_type = user_credentials.type;
    let html;

    if (user_credentials.type === "SIGNUP") {
      const check_user = await UserModel.findOne({ email: user_email });

      if (check_user != null) {
        return res.send("Email already exists").end();
      }
      html = await fs.readFile("src/views/verifyOtp.html", "utf8");
    } else if (user_credentials.type === "resetpassword") {
      const check_user = await UserModel.findOne({ email: user_email });
      if (check_user == null) {
        return res.send("E-mail not found").end();
      } else {
        html = await fs.readFile("src/views/Password_Reset.html", "utf8");
      }
    } else {
      return res.send("Server error while recognizing otp type").end();
    }

    console.log(typeof html);

    const template = handlebars.compile(html); // Compiling HTML file

    const gen_otp = Math.floor(100000 + Math.random() * 900000); // Generate OTP

    const oldDateObj = new Date(new Date());
    const newDateObj = new Date(new Date().getTime());
    newDateObj.setTime(oldDateObj.getTime() + 10 * 60 * 1000);

    // ------ Delete OTP for same Email from database -------------
    await Otp.deleteMany({ email: user_email });

    const mail_data = {
      username: user_name,
      otp: gen_otp,
    };
    const htmlToSend = template(mail_data); // sending data to HTML template

    // ----------------- Insert OTP to database --------------------
    const data = {
      email: user_email,
      otp: gen_otp,
      type: user_type,
      exp: newDateObj,
    };

    const insert_otp = new Otp(data);
    insert_otp.save(function (err, res) {
      if (err) return console.error(err);
    });

    // ----------------- Send mail with nodemailer ------------------
    if (user_credentials.type == "SIGNUP") {
      sendMail(user_email, htmlToSend, "OTP to verify your email");
    } else {
      sendMail(user_email, htmlToSend, "OTP to reset your password");
    }

    res.send("OTP has been sent for e-mail verification");
  } catch (error) {
    console.log(error);
    res.status(500).json({ message: error.message });
  }
};

// -------------------------- Verify EMAIL OTP -------------------------------------------------------------------
export const verifyOTP = async (req, res) => {
  try {
    // console.log("*****| Verifying OTP |*****");
    const info = req.body;

    const newDateObj = new Date();

    let isExpired;
    let isVerified;

    const match = await Otp.findOne({
      email: info.email,
      otp: info.otp,
      type: info.otp_type,
    });

    if (!match) {
      return res.send("Wrong OTP");
    }

    if (newDateObj.getTime() < match.exp.getTime()) {
      isExpired = false;
    } else {
      isExpired = true;
    }

    if (isExpired == true) {
      isVerified = false;
      return res.send("OTP Expired");
    }

    if (match.otp == info.otp) {
      isVerified = true;
      await Otp.deleteMany({ email: info.email });
      return res.send(isVerified);
    }
  } catch (error) {
    res.send(500).json({ message: error.message });
  }
};

// ------------------------------------ Sign Up(REGISTER) ------------------------------------------------
export const createAccount = async (req, res) => {
  try {
    // console.log("*****|  New Account resgistering |*****");

    const data = req.body;
    const user_name = data.name;
    const user_email = data.email;
    const user_password = data.password;
    const user_profile = data.profile;

    const check_email = await UserModel.findOne({
      email: data.email,
    });

    if (check_email) {
      return res.send("Email already exists");
    }

    const hash_password = await bcrypt.hash(user_password, 10);

    const searchLastid = await UserModel.findOne(
      {},
      {},
      { sort: { created_at: -1 } }
    );

    const lastUserId = searchLastid ? searchLastid.id + 1 : 1;

    const user = {
      id: lastUserId,
      name: user_name,
      email: user_email,
      password: hash_password,
      profile: user_profile,
      verified: true,
      created_at: new Date(),
    };

    const add_user = new UserModel(user);

    await add_user.save();
    res.send(true);
  } catch (error) {
    console.log(error);
    res.status(500).json({ message: error.message });
  }
};

// ------------------------------------ Reset OTP, Verification ------------------------------------------------

export const verifyResetOtp = async (otpData) => {
  try {
    // console.log("*****| Verifying Reset Password OTP  | *****");

    const match = await Otp.findOne({
      email: otpData.email,
      otp: otpData.otp,
    });

    if (match == null) {
      res.status(404).send("Not found");
    }

    if (new Date().getTime() > match.exp.getTime()) {
      return { verified: false, error: "OTP Expired" };
    }

    if (match.otp == otpData.otp) {
      await Otp.deleteMany({ email: otpData.email });
      return { verified: true };
    }
  } catch (error) {
    return { verified: false, error: "Something went wrong!" };
  }
};

// ------------------------------------ Reset Password ------------------------------------------------

export const resetpassword = async (req, res) => {
  try {
    const data = req.body;
    // let otp_valid = await verifyResetOtp(data);

    if (data) {
      const hash_password = await bcrypt.hash(data.password, 10);
      await UserModel.updateOne(
        { email: data.email },
        { $set: { password: hash_password } }
      );
      return res.send(true);
    } else {
      return { verified: false, error: "Wrong OTP!" };
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// --------------------------------------- L O G I N  --------------------------------------------------
export const userLogin = async (req, res) => {
  try {
    // console.log("LOGIN");
    const user_credentials = req.body;
    const dateTime = new Date().getTime();
    // search for user in database
    const user_found = await UserModel.findOne({
      email: user_credentials.email,
    });

    if (!user_found) {
      return res.status(400).send({
        message: "User not found.",
      });
    } else {
      bcrypt.compare(
        user_credentials.password,
        user_found.password,
        async function (err, isMatch) {
          if (!isMatch) {
            return res.status(400).send({
              message: "Wrong Password!",
            });
          } else if (isMatch) {
            await UserModel.updateOne(
              { email: user_credentials.email },
              { $push: { logins: new Date() } }
            );
            const jwt_body = {
              id: user_found.id,
              email: user_credentials.email,
              iat: dateTime,
              iss: "Movielust",
            };

            const token = jwt.sign(jwt_body, process.env.SECRET, {
              expiresIn: "15d",
            });

            const res_data = {
              success: true,
              message: "Logged In!",
              id: user_found.id,
              name: user_found.name,
              email: user_found.email,
              profile: user_found.profile,
              token: token,
            };

            res.send(res_data);
          } else {
            if (!isMatch) {
              return res.status(404).send({
                message: "Server error",
              });
            }
          }
        }
      );
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
}

// ---------------------------------------A D M I N   L O G I N  --------------------------------------------------
export const adminLogin = async (req, res) => {
  try {
    // console.log("Admin LOGIN");
    const user_credentials = req.body;
    const dateTime = new Date().getTime();

    const user_found = await AdminSchema.findOne({
      userName: user_credentials.userName,
    });

    if (!user_found) {
      return res.status(400).send({
        message: "User not found.",
      });
    } else {
      if (user_credentials.password === user_found.password) {
        const jwt_body = {
          userName: user_found.userName,
          iat: dateTime,
          iss: "Movielust",
        };
        const token = jwt.sign(jwt_body, process.env.SECRET, {
          expiresIn: "20d",
        });

        const res_data = {
          success: true,
          message: "Logged In!",
          token: token,
          name: user_found.name,
          avatar: user_found.avatar,
        };
        res.send(res_data);
      } else {
        res.send(false);
      }
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
}
// ------------------------------- TASK TO COMPLETE -------------------------------------------------------
// - Send OTP
// - Verify OTP
// - Register (SIGNUP)
// - LOGIN
// - RESET OTP
// - RESET PASSWORD
