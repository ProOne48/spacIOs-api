from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from base.rest_item import RestItem


class Statistics(RestItem):
    """
    Statistics model class
    """

    __tablename__ = 'statistics'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    space_id: Mapped[int] = mapped_column(ForeignKey('space.id'))
    table_id: Mapped[int] = mapped_column(ForeignKey('table.id'))
    start_date: Mapped[datetime] = mapped_column()
    n_people: Mapped[int] = mapped_column()
    n_reservations: Mapped[int] = mapped_column()
    day_of_week: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()

    @classmethod
    def space_statistics(cls, space_id: int):
        """
        Return all statistics Usage from this space
        """
        statistics_data = {
            'total_space_use': cls.total_space_use(space_id),
            'average_space_use': cls.average_space_use(space_id),
            'average_space_use_by_day': cls.average_space_use_by_day(space_id),
        }

        return statistics_data

    @classmethod
    def total_space_use(cls, space_id: int):
        """
        Return the total use of the table
        """
        return cls.session.query(Statistics).filter(Statistics.space_id == space_id).count()

    @classmethod
    def total_table_use(cls, table_id: int):
        """
        Return the total use of the table
        """
        return cls.session.query(Statistics).filter(Statistics.table_id == table_id).count()

    @classmethod
    def average_space_use(cls, space_id: int):
        """
        Return the average use of the Space
        """
        return cls.session.query(func.avg(Statistics.n_people).label('avg_people')).filter(Statistics.space_id == space_id).all()

    @classmethod
    def average_space_use_by_day(cls, space_id: int):
        """
        Return the average use of the Space
        """
        return cls.session.query(Statistics.day_of_week, func.avg(Statistics.n_people).label('avg_people')).group_by(Statistics.day_of_week).filter(Statistics.space_id == space_id).all()

    @classmethod
    def average_table_use(cls, table_id: int):
        """
        Return the average use of the table
        """
        return cls.session.query(Statistics, func.avg(Statistics.duration).label('avg_duration')).group_by(
            Statistics.table_id).filter(Statistics.table_id == cls.table_id).all()

    @classmethod
    def space_use_by_day(cls, space_id: int):
        """
        Return the average use of the table
        """
        return cls.session.query(Statistics.day_of_week).group_by(
            Statistics.day_of_week).filter(Statistics.space_id == space_id).count()
