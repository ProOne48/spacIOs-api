from marshmallow import Schema, fields


class StatisticsUsageByDaySchema(Schema):
    day = fields.String()
    average_space_use = fields.Decimal()
    total_space_use = fields.Integer()


class StatisticsSpaceUsageSchema(Schema):
    """
    Statistics Space Usage schema class
    """
    average_space_use = fields.Decimal()
    average_space_use_by_day = fields.List(fields.Nested(StatisticsUsageByDaySchema))
    total_space_use = fields.Integer()


class StatisticsTableUsageSchema(Schema):

    average_table_use = fields.Method('get_average_table_use')
    total_table_use = fields.Method('get_total_table_use')

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
