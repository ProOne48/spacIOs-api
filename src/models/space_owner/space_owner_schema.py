from marshmallow import Schema, fields


class SpaceOwnerSchema(Schema):
    name = fields.String(required=True, metadata={"description": "Space owner name"})
    email = fields.Email(required=True, metadata={"description": "Space owner email"})
    # spaces = fields.Nested(SpaceListSchema, metadata={"description": "List of spaces owned by the user"})


class SpaceOwnerListSchema(Schema):
    items = fields.Nested(SpaceOwnerSchema, many=True, dump_only=True, metadata={"description": "List of space owners"})
    total = fields.Integer(dump_only=True, metadata={"description": "Total number of space owners"})


class SpaceOwnerCreateSchema(Schema):
    name = fields.String(required=True, metadata={"description": "Space owner name"})
    email = fields.Email(required=True, metadata={"description": "Space owner email"})


class SpaceOwnerGoogleLoginSchema(Schema):
    token = fields.String(required=True, metadata={"description": "Token for Google"})
    email = fields.Email(required=True, metadata={"description": "Email address of the user"})
    name = fields.String(required=True, metadata={"description": "Name of the user"})
