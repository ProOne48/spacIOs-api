from typing import TypedDict

from marshmallow import Schema, fields
from flask_smorest.fields import Upload


class TableSchema(Schema):
    id = fields.Int()
    n_chairs = fields.Int()
    table_number = fields.Int()
    occupied = fields.Bool()
    reservable = fields.Bool()
    space_id = fields.Int()
    qr_code = fields.Str()


class TableListSchema(Schema):
    items = fields.List(fields.Nested(TableSchema))
    total = fields.Int()


class TableCreateSchema(Schema):
    table_number = fields.Int(required=True)
    n_chairs = fields.Int(required=True)
    reservable = fields.Bool(required=True)


class TableQRSchema(Schema):
    qr_code = Upload(required=True)


class TableInputType(TypedDict):
    table_number: int
    n_chairs: int
    reservable: bool
    space_id: int
