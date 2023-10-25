from typing import Optional

from sqlalchemy import ForeignKey, false
from sqlalchemy.orm import Mapped, mapped_column

from base.rest_item import RestItem
from qrcode.image.pil import PilImage
from src.classes.qr_generator import QRGenerator


class Table(RestItem):
    __tablename__ = "table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    table_number: Mapped[int] = mapped_column()
    n_chairs: Mapped[int] = mapped_column()
    reservable: Mapped[bool] = mapped_column(server_default=false())
    space_id: Mapped[int] = mapped_column(ForeignKey("space.id"))
    qr_code: Mapped[Optional[str]] = mapped_column()
    occupied: Mapped[bool] = mapped_column(server_default=false())

    def generate_qr_code(self) -> PilImage:
        return QRGenerator.generate_qr_code(self.space_id, self.id)
