from marshmallow import Schema, fields
from flask_smorest.fields import Upload

from src.models.tables import TableSchema


class SpaceSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    duration = fields.Integer(allow_none=True)
    max_capacity = fields.Integer(required=True)
    space_owner_id = fields.Integer(required=True)
    tables = fields.List(fields.Nested(TableSchema))
    capacity = fields.Integer(required=True)


class SpaceReducedSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    max_capacity = fields.Integer(required=True)
    tables = fields.List(fields.Nested(TableSchema))
    capacity = fields.Integer(required=True)


class SpaceListSchema(Schema):
    items = fields.List(fields.Nested(SpaceSchema))
    total = fields.Integer(required=True)


class SpaceCreateSchema(Schema):
    id = fields.Integer(allow_none=True)
    name = fields.String(required=True)
    description = fields.String()


class SpacePDFSchema(Schema):
    pdf = Upload(required=True)
