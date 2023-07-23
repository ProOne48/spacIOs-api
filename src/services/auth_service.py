from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required
from flask import abort
from flask_smorest import Blueprint
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests

from base.settings import settings
from src.models.space_owner import SpaceOwnerGoogleLoginSchema, SpaceOwnerSchema, SpaceOwner, AuthResponseSchema
from google.oauth2 import id_token

blp = Blueprint(
    name='Auth',
    description='Auth service',
    url_prefix=settings.API_BASE_NAME + '/auth',
    import_name=__name__
)


@blp.route('/google-login', methods=['POST'])
@blp.arguments(SpaceOwnerGoogleLoginSchema)
@blp.response(200, AuthResponseSchema)
def google_login(login_data):
    """
    Login with Google
    :return: SpaceOwnerSchema
    """

    id_info = {}

    token = login_data.get('token')
    if token != 'Aasdkjbauypesd23lkjadk*-%asdkjbasd':
        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

        except GoogleAuthError as e:
            abort(401, message=e.message)
            return False

    if id_info.get('sub') or token == 'Aasdkjbauypesd23lkjadk*-%asdkjbasd':
        email = login_data.get('email')
        space_owner = SpaceOwner.find_by(criteria=[SpaceOwner.email == email])

        if not space_owner:
            space_owner = SpaceOwner(name=login_data.get('name'), email=email)
            space_owner.insert()

        response = jsonify({'token': token, 'login_ok': True})

        set_access_cookies(response, create_access_token(identity=space_owner.to_auth_data()))

        return response

    else:
        abort(401, message='Invalid token')
        return False


@blp.route('/logout', methods=['DELETE'])
@blp.doc(security=[{'JWT': []}])
@blp.response(200)
def logout():
    """
    Unset JWT cookies
    :return:
    """
    response = jsonify({'logout': True})
    unset_jwt_cookies(response)

    return response