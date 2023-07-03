from marshmallow import Schema, fields


class SpaceSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    max_capacity = fields.Integer(required=True)
    space_owner_id = fields.Integer(required=True)
    capacity = fields.Integer(required=True)


class SpaceListSchema(Schema):
    items = fields.List(fields.Nested(SpaceSchema))
    total = fields.Integer(required=True)


class SpaceCreateSchema(Schema):
    name = fields.String(required=True)
    max_capacity = fields.Integer(required=True)
    space_owner_id = fields.Integer(required=True)
    capacity = fields.Integer(required=True)
