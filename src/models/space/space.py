from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from base.rest_item import RestItem
from src.models.tables import Table, TableInputType, TableNumberExistError


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
    capacity: Mapped[Optional[int]] = mapped_column()
    pdf_img: Mapped[Optional[bytes]] = mapped_column()
    tables: Mapped[Optional[List['Table']]] = relationship()

    def check_table_number(self, table_number: int) -> bool:
        """
        Check if the table number already exists in the space
        """
        for t in self.tables:
            if t.table_number == table_number:
                return True
        return False

    def add_table(self, table_data: TableInputType) -> None:
        """
        Add a table to the space
        """
        if self.check_table_number(table_data.get('table_number')):
            raise TableNumberExistError('Table number already exists', 'TABLE_NUMBER_EXISTS')

        table = Table()
        table.add_from_dict(table_data)
        table.space_id = self.id
        table.insert()
        self.tables.append(table)
        self.max_capacity += table.n_chairs

    def delete_table(self, table: Table) -> None:
        """
        Remove a table from the space
        """
        self.max_capacity -= table.n_chairs
        self.tables.remove(table)
        table.delete()

    def edit_table(self, table_data: Table) -> None:
        """
        Edit a table in the space
        """
        for table in self.tables:
            if table.id == table_data.id:
                table = table_data
                table.update()
                break
