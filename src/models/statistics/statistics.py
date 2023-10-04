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

    def total_space_use(self):
        """
        Return the total use of the table
        """
        return self.session.query(Statistics).filter(Statistics.space_id == self.space_id).count()

    def total_table_use(self):
        """
        Return the total use of the table
        """
        return self.session.query(Statistics).filter(Statistics.table_id == self.table_id).count()

    def average_space_use(self):
        """
        Return the average use of the Space
        """
        return self.session.query(Statistics, func.avg(Statistics.duration).label('avg_duration')).group_by(
            Statistics.space_id).filter(Statistics.space_id == self.space_id).all()

    def average_table_use(self):
        """
        Return the average use of the table
        """
        return self.session.query(Statistics, func.avg(Statistics.duration).label('avg_duration')).group_by(
            Statistics.table_id).filter(Statistics.table_id == self.table_id).all()

    def space_use_by_day(self):
        """
        Return the average use of the table
        """
        return self.session.query(Statistics).group_by(
            Statistics.day_of_week).filter(Statistics.space_id == self.space_id).count()
