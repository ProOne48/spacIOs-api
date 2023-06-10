from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from base.rest_item import RestItem

class Space(RestItem):
    """
    Space model class
    """
    __tablename__ = 'space'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    max_capacity: Mapped[int] = mapped_column()
    space_owner_id: Mapped[int] = mapped_column(ForeignKey('space_owner.id'))
    capacity: Mapped[Optional[int]] = mapped_column()
