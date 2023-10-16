import NodeMailer from "nodemailer";
import dotenv from "dotenv";

dotenv.config();

const transporter = NodeMailer.createTransport({
  host: process.env.MAIL_SERVER,
  port: process.env.MAIL_PORT,
  secure: true,
  ignoreTLS: true,
  auth: {
    user: process.env.MAIL_EMAIL,
    pass: process.env.MAIL_PASSWORD,
  },
});

export { transporter };

export const sendMail = (to, htmlToSend, subject) => {
  return new Promise((resolve, reject) => {
    if (!htmlToSend)
      return reject(new Error("Failed because mail content was empty"));
    const options = {
      from: process.env.MAIL_EMAIL,
      to,
      subject,
      html: htmlToSend, // html body
    };
    return transporter.sendMail(options, (error, info) => {
      if (error) return reject(error);
      return resolve(info);
    });
  });
};

export const verifyTransport = async () =>

  new Promise((resolve) => {
    (async () => {
      try {
        await transporter.verify();
        console.log("Mail server verified.");
        resolve();
      } catch (err) {
        console.log("Mail server error:", err);
        throw new Error(err);
      }
    })();
  })

