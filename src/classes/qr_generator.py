import qrcode
import pyshorteners
from qrcode.image.pil import PilImage
from qrcode.image.pure import PyPNGImage


class QRGenerator:
    @staticmethod
    def generate_qr_code(space_id, table_id) -> PilImage:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=10,
            border=4,
        )

        url = 'http://localhost:4200/' + str(space_id) + '/' + str(table_id)

        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(url)

        qr.add_data(short_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        return img
