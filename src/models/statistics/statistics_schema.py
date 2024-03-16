from marshmallow import Schema, fields


class StatisticsSchema(Schema):
    id = fields.Integer(dump_only=True)
    space_id = fields.Integer()
    table_id = fields.Integer()
    start_date = fields.DateTime()
    n_people = fields.Integer()
    day_of_week = fields.String()
    duration = fields.Integer()


class StatisticsUsageByDaySchema(Schema):
    day = fields.String(allow_none=True)
    average_space_use = fields.Decimal(required=True)
    total_space_use = fields.Integer(required=True)
    hour = fields.Integer(allow_none=True)


class StatisticsSpaceUsageSchema(Schema):
    """
    Statistics Space Usage schema class
    """

    average_space_use = fields.Decimal()
    average_space_use_per_day = fields.List(fields.Nested(StatisticsUsageByDaySchema))
    total_space_use = fields.Integer()


class StatisticsTableUsageSchema(Schema):
    average_table_use = fields.Method("get_average_table_use")
    total_table_use = fields.Method("get_total_table_use")

    @staticmethod
    def get_average_table_use(obj):
        return obj.average_table_use(obj.table_id)

    @staticmethod
    def get_total_table_use(obj):
        return obj.total_table_use(obj.table_id)


class StatisticsUsageListSchema(Schema):
    """
    Statistics List schema class
    """

    items = fields.List(fields.Nested(StatisticsSpaceUsageSchema))
    total = fields.Int()
