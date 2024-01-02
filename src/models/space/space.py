import threading
from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from base.rest_item import RestItem
from src.models.tables import (
    Table,
    TableInputType,
    TableNumberExistError,
    TableAlreadyOccupiedError,
)
from base.settings import settings


class Space(RestItem):
    """
    Space model class
    """

    __tablename__ = "space"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    max_capacity: Mapped[int] = mapped_column()
    duration: Mapped[Optional[int]] = mapped_column()
    space_owner_id: Mapped[int] = mapped_column(ForeignKey("space_owner.id"))
    capacity: Mapped[Optional[int]] = mapped_column()
    pdf_img: Mapped[Optional[bytes]] = mapped_column()
    tables: Mapped[Optional[List["Table"]]] = relationship()

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
        if self.check_table_number(table_data.get("table_number")):
            raise TableNumberExistError(
                "Table number already exists", "TABLE_NUMBER_EXISTS"
            )

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

    def update_table(self, table_data: Table) -> None:
        """
        Edit a table in the space
        """
        for table in self.tables:
            if table.id == table_data.id:
                table = table_data
                table.update()
                self.update()
                break

    def occupy_table(self, table_id: int) -> None:
        """
        Occupy a table
        """
        duration = self.duration if self.duration else settings.DEFAULT_DURATION
        for table in self.tables:
            if table.id == table_id:
                if table.occupied:
                    raise TableAlreadyOccupiedError(
                        "Table already occupied", "TABLE_ALREADY_OCCUPIED"
                    )

                table.occupied = True
                self.capacity += (
                    table.n_chairs
                    if self.capacity + table.n_chairs < self.max_capacity
                    else 0
                )
                self.update_table(table)
                threading.Timer(
                    duration * settings.SECONDS_TO_MINUTES,
                    self.table_free,
                    args=[table_id],
                ).start()
                break

    def table_free(self, table_id: int) -> None:
        """
        Free a table
        """
        table = Table.find(table_id)
        print("----------------Table being free---------------------\n", table.occupied)
        table.occupied = False
        self.capacity -= table.n_chairs if self.capacity - table.n_chairs > 0 else 0
        print("----------------Table free---------------------\n", table.occupied)
        self.update_table(table)
