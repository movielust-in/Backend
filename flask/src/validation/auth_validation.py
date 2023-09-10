from marshmallow import Schema, fields, validate
from .common_validation import (
    Email,
    Name,
    Otp,
    Password,
)


class UserRegister(Schema):
    name = Name
    email = Email
    profile = fields.String(
        required=True,
        error_messages={
            "required": "Name is required!"
        },
        validate=validate.Length(min=1, max=1000),
    )
    password = Password


class UserLogin(Schema):
    email = Email
    password = Password


class VerifyEmailOTP(Schema):
    name = Name
    email = Email


class ResetOTP(Schema):
    email = Email


class ResetPassword(Schema):
    email = Email
    password = Password
    otp = Otp


class AdminAuth(Schema):
    userName = fields.String(
        required=True,
        error_messages={
            "required": "userName is required!"
        },
        validate=validate.Length(min=1, max=32),
    )
    password = Password
