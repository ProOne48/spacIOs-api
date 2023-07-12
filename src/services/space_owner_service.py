from flask import abort
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from base.settings import settings
from src.app import context
from src.models.space_owner import SpaceOwner, SpaceOwnerListSchema, SpaceOwnerSchema, CreateSpaceOwnerSchema

api_url = settings.API_BASE_NAME + '/space-owner'
api_name = 'SpaceOwner'
api_description = 'SpaceOwner service'

blp = Blueprint(
    name=api_name,
    description=api_description,
    url_prefix=api_url,
    import_name=__name__
)


@blp.route('', methods=['GET'])
@blp.response(200, SpaceOwnerListSchema)
def get_space_owners():
    """
    Get all space owners
    :return: A list of space owners
    """
    items, total = SpaceOwner.list()
    return {'items': items, 'total': total}


@blp.route('/<int:space_owner_id>', methods=['GET'])
@blp.response(200, SpaceOwnerSchema)
def get_space_owner_by_id(space_owner_id: int):
    """
    Get a space owner by id
    :param space_owner_id: Space owner id
    :return: SpaceOwnerSchema
    """
    return SpaceOwner.find(space_owner_id)


@blp.route('/actual-space-owner', methods=['GET'])
@jwt_required()
@blp.response(200, SpaceOwnerSchema)
def get_actual_user():
    """
    Get actual user
    :return: SpaceOwnerSchema
    """
    space_owner = SpaceOwner()
    try:
        space_owner = SpaceOwner.find(context.get_user_id())
    except Exception as e:
        abort(404, message=e.message)

    return space_owner


@blp.route('', methods=['POST'])
@blp.arguments(CreateSpaceOwnerSchema)
@blp.response(200, SpaceOwnerSchema)
def create_space_owner(space_owner_data):
    """
    Create a space owner
    :param space_owner_data: SpaceOwnerCreateSchema
    :return: SpaceOwnerSchema
    """
    space_owner = SpaceOwner()
    space_owner.add_from_dict(space_owner_data)
    try:
        space_owner.insert()
    except Exception as e:
        abort(400, message=e.message)

    return space_owner


@blp.route('/<int:space_owner_id>', methods=['PUT'])
@jwt_required()
@blp.arguments(SpaceOwnerSchema)
@blp.response(200, SpaceOwnerSchema)
def update_space_owner(space_owner_data: dict, space_owner_id: int):
    """
    Update a space owner
    :param space_owner_data: SpaceOwnerSchema
    :param space_owner_id: Space owner id
    :return: SpaceOwnerSchema
    """
    space_owner = SpaceOwner.find(space_owner_id)
    if space_owner is None:
        abort(404, message='Space owner not found')
    space_owner.add_from_dict(space_owner_data)
    try:
        space_owner.update()
    except Exception as e:
        abort(400, message=e.message)

    return space_owner


@blp.route('/<int:space_owner_id>', methods=['DELETE'])
@jwt_required()
@blp.response(204)
def delete_space_owner(space_owner_id: int):
    """
    Delete a space owner
    :param space_owner_id: Space owner id
    :return: None
    """
    space_owner = SpaceOwner.find(space_owner_id)
    if space_owner is None:
        abort(404, message='Space owner not found')
    try:
        space_owner.delete()
    except Exception as e:
        abort(400, message=e.message)
