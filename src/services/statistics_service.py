from datetime import datetime

from flask import request
from flask_smorest import Blueprint, abort

from base.settings import settings
from src.models.statistics import (
    StatisticsSpaceUsageSchema,
    StatisticsSchema,
    StatisticsFormat,
    Statistics,
)

api_url = settings.API_BASE_NAME + "/statistics"
api_name = "Statistics"
api_description = "Statistics service"

blp = Blueprint(
    name=api_name, description=api_description, url_prefix=api_url, import_name=__name__
)


@blp.route("", methods=["GET"])
@blp.response(200, StatisticsSpaceUsageSchema)
def get_statistics():
    """
    Get all statistics
    :return: A list of statistics
    """
    items, total = Statistics.list()
    return {"items": items, "total": total}


@blp.route("/<int:space_id>", methods=["GET"])
@blp.response(200, StatisticsSpaceUsageSchema)
def get_statistics_by_space(space_id: int):
    """
    Get statistics by space
    :param space_id: Space id
    :return: A list of statistics
    """
    time = request.args.get("time", datetime(2010, 1, 1).isoformat())
    date = datetime.fromisoformat(time.replace("Z", "+01:00"))
    statistics_format = request.args.get("format", StatisticsFormat.DAY.value)

    return Statistics.space_statistics(space_id, date, statistics_format)


@blp.route("", methods=["POST"])
@blp.arguments(StatisticsSchema)
@blp.response(201)
def create_statistics(statistics_data: StatisticsSchema):
    """
    Create a new statistics
    :param statistics_data: StatisticsSchema
    :return: StatisticsSchema
    """
    statistics = Statistics()
    statistics.add_from_dict(statistics_data)
    try:
        statistics.insert()
    except Exception as e:
        abort(400, message=str(e))
