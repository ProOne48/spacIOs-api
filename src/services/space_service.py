import io

from flask import request, send_file
from flask_smorest import abort
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from base.settings import settings
from src.app import context
from src.models.space import Space, SpaceSchema, SpaceListSchema, SpaceCreateSchema, SpacePDFSchema
from src.models.tables import TableCreateSchema, Table

blp = Blueprint(
    name='Space',
    description='Space service',
    url_prefix=settings.API_BASE_NAME + '/space',
    import_name=__name__
)


@blp.route('', methods=['GET'])
@blp.response(200, SpaceListSchema)
def get_spaces():
    """
    Get all spaces
    :return: A list of spaces
    """
    items, total = Space.list()
    return {'items': items, 'total': total}


@blp.route('/actual-spaces', methods=['GET'])
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200, SpaceListSchema)
def get_actual_spaces():
    """
    Get actual spaces
    :return: A list of spaces
    """
    items, total = Space.list(criteria=[Space.space_owner_id == context.get_user_id()])

    return {'items': items, 'total': total}


@blp.route('/<int:space_id>', methods=['GET'])
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200, SpaceSchema)
def get_space_by_id(space_id: int):
    """
    Get a space by id
    :param space_id: Space id
    :return: SpaceSchema
    """
    return Space.find(space_id)


@blp.route('', methods=['POST'])
@blp.arguments(SpaceCreateSchema)
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200, SpaceSchema)
def create_space(space_data):
    """
    Create a space
    :param space_data: SpaceCreateSchema
    :return: SpaceSchema
    """
    space = Space()
    space.add_from_dict(space_data)
    space.space_owner_id = context.get_user_id()
    space.capacity = 0
    space.max_capacity = 0
    try:
        space.insert()
    except Exception as e:
        abort(400, message=e)

    return space


@blp.route('/<int:space_id>/table', methods=['PUT'])
@blp.arguments(TableCreateSchema)
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200, SpaceSchema)
def add_table(table_data, space_id: int):
    """
    Add a table to a space
    :param table_data: CreateTableSchema
    :param space_id: Space id
    :return: SpaceSchema
    """
    space = Space.find(space_id)
    space.add_table(table_data)

    space.update()

    return space


@blp.route('/<int:space_id>/table/<int:table_id>', methods=['DELETE'])
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(204, SpaceSchema)
def delete_table(space_id, table_id):
    """
    Delete a table from a space
    :param space_id: Space id
    :param table_id: Table id
    :return: SpaceSchema
    """
    space = Space.find(space_id)
    table = Table.find(table_id)
    space.delete_table(table)

    space.update()

    return space


@blp.route('/<int:space_id>/table/<int:table_id>', methods=['PATCH'])
@blp.arguments(TableCreateSchema)
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200, SpaceSchema)
def edit_table(table_data, space_id: int, table_id: int):
    """
    Edit a table from a space
    :param table_data: CreateTableSchema
    :param space_id: Space id
    :param table_id: Table id
    :return: SpaceSchema
    """
    space = Space.find(space_id)
    table = Table.find(table_id)
    space.edit_table(table, table_data)


    return space


@blp.route('/<int:space_id>', methods=['PUT'])
@blp.arguments(SpaceCreateSchema)
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200, SpaceSchema)
def edit_space(space_data, space_id: int):
    """
    Update a space
    :param space_data: SpaceSchema
    :param space_id: Space id
    :return: SpaceSchema
    """
    space = Space.find(space_id)
    space.add_from_dict(space_data)
    try:
        space.update()
    except Exception as e:
        abort(400, message=e.message)

    return space


@blp.route('/<int:space_id>', methods=['DELETE'])
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(204)
def delete_space(space_id: int):
    """
    Delete a space
    :param space_id: Space id
    :return: None
    """
    space = Space.find(space_id)
    if not space:
        abort(404, message='Space not found')
    try:
        space.delete()
    except Exception as e:
        abort(400, message=e.message)

    return None


@blp.route('/<int:space_id>/pdf', methods=['GET'])
@blp.response(200)
def get_pdf(space_id: int):
    """
    Get pdf image for a space
    :param space_id: Space id
    :return: SpacePDFSchema
    """
    space = Space.find(space_id)
    if not space:
        abort(404, message='Space not found')

    if space.pdf_img:
        pdf_bytes = io.BytesIO(space.pdf_img)

    filename = space.name + '.pdf'

    print(pdf_bytes)

    return send_file(pdf_bytes, download_name=filename, mimetype='application/pdf')


@blp.route('/<int:space_id>/pdf', methods=['PUT'])
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.arguments(SpacePDFSchema, location='files')
@blp.response(200)
def upload_pdf(file_data, space_id: int):
    """
    Upload a pdf image for a space
    :param file_data: SpacePDFSchema
    :param space_id: Space id
    :return: None
    """
    space = Space.find(space_id)
    if not space:
        abort(404, message='Space not found')

    space.pdf_img = request.files['pdf'].read()

    try:
        space.update()
    except Exception as e:
        abort(400, message=e.message)

    return None
