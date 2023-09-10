import jwt from "jsonwebtoken";

export default function (req, res, next) {
  try {
    const bearerToken = req.header("Authorization");
    if (!bearerToken) return res.status(401).json({ msg: "No token!" });

    const token = bearerToken.split(" ");

    if (token[0] !== "Bearer") {
      return res.status(401).json({ msg: "Invalid Token!" });
    }
    const decodedToken = jwt.verify(token[1], process.env.SECRET);

    if (!decodedToken) return res.status(401).send(error);

    req.user = decodedToken;

    next();
  } catch (error) {
    return res.status(401).send(error);
  }
}
