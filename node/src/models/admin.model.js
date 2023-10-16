import pkg from 'mongoose';

const { Schema, model } = pkg;

const AdminSchema = new Schema({
    id: {
        type: String,
    },
    name: {
        type: String,
    },
    userName: {
        type: String,
    },
    avatar: {
        type: String,
    },
    password: {
        type: String,
    },
    authorization: {
        type: String,
    },
    created_at: {
        type: String,
    },
});

export default model('admin_login', AdminSchema, 'admin');
