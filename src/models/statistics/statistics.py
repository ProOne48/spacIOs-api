from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from base.rest_item import RestItem


# Enum for the statistics format by day, week or hour
class StatisticsFormat(Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"


class Statistics(RestItem):
    """
    Statistics model class
    """

    __tablename__ = "statistics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    space_id: Mapped[int] = mapped_column(ForeignKey("space.id"))
    table_id: Mapped[int] = mapped_column(ForeignKey("table.id"))
    start_date: Mapped[datetime] = mapped_column(default=func.now())
    n_people: Mapped[int] = mapped_column()
    day_of_week: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()

    @classmethod
    def space_statistics(
        cls, space_id: int, from_date: datetime, format: StatisticsFormat
    ):
        """
        Return all statistics Usage from this space
        """

        avg_space_use_by_day = cls.average_space_use_by_day(space_id, from_date, format)

        # TODO: show porcentage of use of the space
        statistics_data = {
            "total_space_use": cls.total_space_use(space_id, from_date),
            "average_space_use": cls.average_space_use(space_id, from_date),
            "average_space_use_per_day": cls.formating_space_use(
                avg_space_use_by_day, format
            ),
        }

        return statistics_data

    # TODO: show for hours for days
    @classmethod
    def total_space_use(cls, space_id: int, from_date: datetime):
        """
        Return the total use of the table
        """
        return (
            cls.session.query(Statistics)
            .filter(Statistics.space_id == space_id, Statistics.start_date > from_date)
            .count()
        )

    @classmethod
    def total_table_use(cls, table_id: int, from_date: datetime):
        """
        Return the total use of the table
        """
        return (
            cls.session.query(Statistics)
            .filter(Statistics.table_id == table_id, Statistics.start_date > from_date)
            .count()
        )

    @classmethod
    def average_space_use(cls, space_id: int, from_date: datetime):
        """
        Return the average use of the Space
        """
        # TODO: do it for the last week or month?
        return (
            cls.session.query(func.sum(Statistics.n_people))
            .filter(Statistics.space_id == space_id, Statistics.start_date > from_date)
            .first()[0]
        )

    @classmethod
    def average_space_use_by_day(
        cls, space_id: int, from_date: datetime, statistics_format: StatisticsFormat
    ):
        """
        Return the average use of the Space
        """

        if statistics_format == StatisticsFormat.HOUR.value:
            query = (
                cls.session.query(
                    func.avg(Statistics.n_people),
                    func.sum(Statistics.n_people),
                    func.extract("hour", Statistics.start_date),
                )
                .filter(
                    Statistics.space_id == space_id, Statistics.start_date > from_date
                )
                .group_by(func.extract("hour", Statistics.start_date))
            )
        else:
            query = (
                cls.session.query(
                    Statistics.day_of_week,
                    func.avg(Statistics.n_people),
                    func.sum(Statistics.n_people),
                )
                .filter(
                    Statistics.space_id == space_id, Statistics.start_date > from_date
                )
                .group_by(Statistics.day_of_week)
            )

        return query.all()

    @classmethod
    def average_table_use(cls, table_id: int, from_date: datetime):
        """
        Return the average use of the table
        """
        return (
            cls.session.query(
                Statistics, func.avg(Statistics.duration).label("avg_duration")
            )
            .filter(Statistics.table_id == table_id, Statistics.start_date > from_date)
            .group_by(Statistics.table_id)
            .all()
        )

    @classmethod
    def space_use_by_day(cls, space_id: int, from_date: datetime = None):
        """
        Return the average use of the table
        """
        return (
            cls.session.query(Statistics.day_of_week)
            .filter(Statistics.space_id == space_id, Statistics.start_date > from_date)
            .group_by(Statistics.day_of_week)
            .count()
        )

    @staticmethod
    def formating_space_use_by_day(data):
        formatted_data = []
        for item in data:
            formatted_day = {
                "day": item[0],
                "average_space_use": item[1],
                "total_space_use": item[2],
            }
            formatted_data.append(formatted_day)

        return formatted_data

    @staticmethod
    def formating_space_use_by_hour(data):
        formatted_data = []
        for item in data:
            formatted_day = {
                "average_space_use": item[0],
                "total_space_use": item[1],
                "hour": item[2],
            }
            formatted_data.append(formatted_day)

        return formatted_data

    @classmethod
    def formating_space_use(cls, data, statistics_format: StatisticsFormat):
        """
        Return the average use of the table formatted
        """
        if statistics_format == StatisticsFormat.HOUR.value:
            return cls.formating_space_use_by_hour(data)
        elif statistics_format == StatisticsFormat.DAY.value:
            return cls.formating_space_use_by_day(data)
