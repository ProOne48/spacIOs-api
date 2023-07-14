from typing import Optional

from sqlalchemy import ForeignKey, false
from sqlalchemy.orm import Mapped, mapped_column

from base.rest_item import RestItem
from qrcode.image.pil import PilImage


class Table(RestItem):
    __tablename__ = 'table'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    n_chairs: Mapped[int] = mapped_column()
    reservable: Mapped[bool] = mapped_column(server_default=false())
    space_id: Mapped[int] = mapped_column(ForeignKey('space.id'))
    qr_code: Mapped[Optional[str]] = mapped_column()
    occupied: Mapped[bool] = mapped_column()
