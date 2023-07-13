from marshmallow import Schema, fields


class TableSchema(Schema):
    id = fields.Int(dump_only=True)
    n_chairs = fields.Int()
    reservable = fields.Bool()
    space_id = fields.Int()
    qr_code = fields.Str()


class TableListSchema(Schema):
    items = fields.List(fields.Nested(TableSchema))
    total = fields.Int()


class TableCreateSchema(Schema):
    n_chairs = fields.Int()
    reservable = fields.Bool()
    space_id = fields.Int()
