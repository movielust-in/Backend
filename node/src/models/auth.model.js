import pkg from "mongoose";
const { Schema, model } = pkg;

const RequestOTP = new Schema(
  {
    email: {
      type: String,
      required: true,
    },
    otp: {
      type: Number,
      required: true,
    },
    type: {
      type: String,
    },
    exp: {
      type: Date,
    },
  },
  {
    versionKey: false,
  }
);

export default model("RequestOtp", RequestOTP, "otp");
