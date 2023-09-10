from marshmallow import fields, validate, Schema


Email = fields.Email(
    required=True,
    error_message={
        "required": "Email is required!"
    },
)

Name = fields.String(
    required=True,
    error_messages={
        "required": "Name is required!"
    },
    validate=validate.Length(min=1, max=40),
)

Password = fields.String(
    required=True,
    error_messages={
        "required": "Password not present!"
    },
    validate=validate.Length(min=6, max=30),
)

Otp = fields.Integer(
    required=True,
    validate=validate.Range(99999, 999999),
)

Boolean = fields.Boolean(required=True)

Url = fields.Url(required=True)

String = fields.String(required=True)

Content_Id = fields.Integer(
    required=True,
    error_message={"required": "id is required!"},
)

Content_Type = fields.String(
    required=True,
    error_messages={
        "required": "type is required!",
        "OneOf": "type can only take values 'movie' or 'tv'",
    },
    validate=validate.OneOf(["movie", "tv"]),
)


class Content(Schema):
    content_id: fields.Integer(
        required=True,
        error_message={
            "required": "id is required!"
        },
    )
    type: fields.String(
        required=True,
        error_messages={
            "required": "type is required!",
            "OneOf": "type can only take values 'movie' or 'tv'",
        },
        validate=validate.OneOf(["movie", "tv"]),
    )


def custom_field(
    required=True, error=None, valid=None
):
    return fields.String(
        required=required,
        error_messages=error,
        validate=valid,
    )
