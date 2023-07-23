from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from base.rest_item import RestItem
from src.models.tables import Table


class Space(RestItem):
    """
    Space model class
    """
    __tablename__ = 'space'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    max_capacity: Mapped[int] = mapped_column()
    space_owner_id: Mapped[int] = mapped_column(ForeignKey('space_owner.id'))
    tables: Mapped[Optional[List['Table']]] = relationship() #noqa: F821
    capacity: Mapped[Optional[int]] = mapped_column()


    def add_table(self, table: Table) -> None:
        """
        Add a table to the space
        """
        table.space_id = self.id
        self.tables.append(table)
        self.capacity += table.n_chairs
        self.max_capacity += table.n_chairs

    def delete_table(self, table: Table) -> None:
        """
        Remove a table from the space
        """
        self.tables.remove(table)
        self.capacity -= table.capacity
        self.max_capacity -= table.capacity

    def edit_table(self, table_data: Table) -> None:
        """
        Edit a table in the space
        """
        for table in self.tables:
            if table.id == table_data.id:
                table = table_data
                table.update()
                break
