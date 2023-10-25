from flask_smorest import Blueprint, abort

from base.settings import settings
from src.models.statistics import StatisticsSpaceUsageSchema
from src.models.statistics.statistics import Statistics
from src.models.statistics.statistics_schema import StatisticsSchema

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
    return Statistics.space_statistics(space_id)


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
