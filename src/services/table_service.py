import io

from flask import abort, send_file
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
import qrcode

from base.settings import settings
from src.models.tables import Table, TableSchema, TableListSchema, TableCreateSchema

blp = Blueprint(
    name='Table',
    description='Table service',
    url_prefix=settings.API_BASE_NAME + '/table',
    import_name=__name__
)


@blp.route('', methods=['GET'])
@blp.response(200, TableListSchema)
def get_tables():
    """
    Get all tables
    :return: A list of tables
    """

    tables, total = Table.list()
    return {'items': tables, 'total': total}


@blp.route('/<int:table_id>', methods=['GET'])
@blp.response(200, TableSchema)
def get_table_by_id(table_id: int):
    """
    Get a table by id
    :param table_id: Table id
    :return: TableSchema
    """
    return Table.find(table_id)


@blp.route('/<int:table_id>/qr-code', methods=['GET'])
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200)
def get_qrcode(table_id: int):
    """
    Get a QR code by table id
    :param table_id: Table id
    :return: QR code
    """
    table = Table.find(table_id)
    qr_code = table.generate_qr_code()

    qr_code_bytes = io.BytesIO()
    qr_code.save(qr_code_bytes, 'JPEG')
    filename = 'table-number-' + str(table.table_number) + '.jpeg'
    qr_code_bytes.seek(0)

    return send_file(qr_code_bytes, mimetype='image/jpeg', download_name=filename, as_attachment=True)
