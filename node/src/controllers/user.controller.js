import { AvatarModel, UserModel } from '../models/user.model.js';

export const getUserProfile = async (req, res) => {
    try {
        const user_id = req.user.email;

        const user = await UserModel.findOne({ email: user_id });

        if (user) {
            await UserModel.updateOne(
                { email: user.email },
                { $push: { visits: new Date() } }
            );
            const user_data = {
                success: true,
                message: 'Login OK',
                email: user.email,
                profile: user.profile,
                name: user.name,
                id: user.id,
            };
            res.send(user_data);
        } else {
            res.status(401).json({ message: 'Unauthorized' });
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

export const updateAvatar = async (req, res) => {
    try {
        const user = req.user.email;
        const a_id = req.body.avatar;

        const link = await AvatarModel.findOne({ id: a_id });
        await UserModel.updateOne(
            { email: user },
            { $set: { profile: link.link } }
        );
        return res.send(true);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
};

export const deleteuser = async (req, res) => {
    try {
        const user_id = req.id;
        await UserModel.deleteOne({ email: user_id });
        res.send(true);
    } catch {
        res.status(500).json({ message: err.message });
    }
};
// --------------------------- Watched  -------------------------------------------

export const getWatched = async (req, res) => {
    try {
        // console.log("Get Watched");
        const user_email = req.user.email;

        const watched_obj = await UserModel.findOne({ email: user_email });

        const watched_data = watched_obj.watched.slice(-20).reverse();

        res.send(watched_data);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

export const addWatched = async (req, res) => {
    try {
        // console.log("Add to watched");
        const user_email = req.user.email;

        const watched_obj = req.body;
        let already_exists;

        const data = {
            content_id: watched_obj.content_id,
            type: watched_obj.type,
            time: new Date(),
        };

        const match = {
            content_id: watched_obj.content_id,
            type: watched_obj.type,
        };

        if (watched_obj.type === 'tv') {
            (data['season'] = watched_obj.season.toString()),
                (data['episode'] = watched_obj.episode.toString()),
                (match['season'] = watched_obj.season),
                (match['episode'] = watched_obj.episode);
        }

        already_exists = await UserModel.find({
            email: user_email,
            watched: { $elemMatch: match },
        });

        if (already_exists.length > 0) {
            return res.send(false);
        } else if (already_exists.length == 0) {
            already_exists = await UserModel.updateOne(
                { email: user_email },
                { $push: { watched: data } }
            );

            return res.send(true);
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

// --------------------------- WATCHLIST -------------------------------------------

export const getWatchlist = async (req, res) => {
    try {
        const user_email = req.user.email;
        const watchlist_obj = await UserModel.findOne({ email: user_email });

        const watchlist_data = watchlist_obj.watchlist;

        res.send(watchlist_data);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
};

export const addToWatchlist = async (req, res) => {
    try {
        const user_email = req.user.email;
        const c_id = req.body.content_id;
        const c_type = req.body.type;
        const data = {
            content_id: c_id,
            type: c_type,
        };

        const add = await UserModel.updateOne(
            { email: user_email },
            { $push: { watchlist: data } }
        );
        if (add) {
            res.send(true);
        }
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
};

export const removeWatchlist = async (req, res) => {
    try {
        const user_email = req.user.email;
        const c_id = req.body.content_id;
        const c_type = req.body.type;
        const remove = await UserModel.updateOne(
            { email: user_email },
            {
                $pull: {
                    watchlist: {
                        content_id: c_id,
                        type: c_type,
                    },
                },
            }
        );
        if (remove) {
            res.send(true);
        }
    } catch (err) {
        res.status(err).json({ message: err.message });
    }
};

export const deleteWatched = async (req, res) => {
    const user_data = req.body;
    await UserModel.updateOne(
        { email: user_data.email },
        {
            $pull: {
                watched: {
                    content_id: user_data.content_id,
                },
            },
        }
    );

    res.send(true);
};
