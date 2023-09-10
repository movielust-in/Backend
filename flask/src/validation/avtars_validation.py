from marshmallow import Schema

from src.validation.common_validation import Url


class AvtarLink(Schema):
    link = Url
