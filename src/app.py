from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api, abort

from base.db_manager import Session
from base.settings import settings

app = Flask(settings.APP_NAME)

app.secret_key = settings.SECRET_KEY

jwt = JWTManager(app)

app.config.update(settings.OPENAPI_CONFIG)

api = Api(app)

if settings.ENABLE_CORS:
    from flask_cors import CORS

    CORS(app, supports_credentials=True)

if settings.DEBUG_SQL > 0:
    from easy_profile import EasyProfileMiddleware

    app.wsgi_app = EasyProfileMiddleware(app.wsgi_app)

from src.services import space_owner_service

# TODO: Add the blueprints to the app

api.register_blueprint(space_owner_service.blp)


@app.errorhandler(500)
def internal_error_handler(error: Exception):

    Session.rollback()
    abort(500, message="The server has an unexpected error.")
