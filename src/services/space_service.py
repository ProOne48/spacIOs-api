from flask import abort
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from base.settings import settings
from src.app import context
from src.models.space import Space, SpaceSchema, SpaceListSchema, SpaceCreateSchema

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
    space_owner_id = context.get_user_id()
    items, total = Space.list(criteria=[Space.space_owner_id == space_owner_id])
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
    try:
        space.insert()
    except Exception as e:
        abort(400, message=e.message)

    return space


@blp.route('/<int:space_id>', methods=['PUT'])
@blp.arguments(SpaceSchema)
@jwt_required()
@blp.doc(security=[{'JWT': []}])
@blp.response(200, SpaceSchema)
def update_space(space_data, space_id: int):
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
    try:
        space.delete()
    except Exception as e:
        abort(400, message=e.message)

    return None
