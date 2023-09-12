import { AvatarModel } from "../models/user.model.js";

export const getAllAvatar = async (req, res) => {
  try {
    const link = await AvatarModel.find({}, { _id: 0 });
    res.send(link);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
