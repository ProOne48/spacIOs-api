from flask import abort
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

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


@blp.route('', methods=['POST'])
@blp.arguments(TableCreateSchema)
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200, TableSchema)
def create_table(table_data):
    """
    Create a table
    :param table_data: TableCreateSchema
    :return: TableSchema
    """
    table = Table()
    table.add_from_dict(table_data)

    try:
        table.insert()
    except Exception as e:
        return abort(400, message=e.message)

    return table


@blp.route('/<int:table_id>', methods=['PUT'])
@blp.arguments(TableSchema)
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200, TableSchema)
def update_table(table_data, table_id: int):
    """
    Update a table by id
    :param table_data: TableSchema
    :param table_id: Table id
    :return: TableSchema
    """
    table = Table.find(table_id)
    table.add_from_dict(table_data)

    try:
        table.update()
    except Exception as e:
        return abort(400, message=e.message)

    return table


@blp.route('/<int:table_id>', methods=['DELETE'])
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200)
def delete_table(table_id: int):
    """
    Delete a table by id
    :param table_id: Table id
    :return: TableSchema
    """
    return Table.delete(table_id)
