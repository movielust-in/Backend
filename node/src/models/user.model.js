import pkg from "mongoose";
const { Schema, model } = pkg;

const UserSchema = new Schema({
  id: {
    type: Number,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  password: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
  },
  profile: {
    type: String,
    default: "",
  },
  verified: {
    type: String,
    required: true,
  },
  created_at: {
    type: String,
  },
  logins: [
    {
      type: String,
    },
  ],
  watchlist: [
    {
      type: Object,
    },
  ],
  visits: [
    {
      type: String,
    },
  ],
  watched: [
    {
      type: Object,
    },
  ],
});

const AvatarSchema = new Schema({
  id: {
    type: Number,
    required: true,
  },
  link: {
    type: String,
  },
});

const UserModel = model("User", UserSchema, "user");

const AvatarModel = model("Avatar", AvatarSchema, "avatars");

export { UserModel, AvatarModel };
