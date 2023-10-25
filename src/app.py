from datetime import timedelta

from flask import Flask, g
from flask_jwt_extended import JWTManager
from flask_smorest import Api, abort

from base.context import Context
from base.db_manager import Session
from base.settings import settings
from src.models.space_owner import UserAuthSchema

app = Flask(settings.APP_NAME)

context = Context()

app.secret_key = settings.SECRET_KEY

app.config["JWT_SECRET_KEY"] = settings.SECRET_KEY
app.config["JWT_ACCESS_COOKIE_PATH"] = settings.API_BASE_NAME
app.config["JWT_COOKIE_CSRF_PROTECT"] = not settings.DEBUG_MODE
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_COOKIE_SAMESITE"] = "Strict"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=settings.SESSION_DURATION_HRS)

jwt = JWTManager(app)

app.config.update(settings.OPENAPI_CONFIG)

api = Api(app)

if settings.ENABLE_CORS:
    from flask_cors import CORS

    CORS(app, supports_credentials=True, origins=settings.CORS_ORIGINS)

if settings.DEBUG_SQL > 0:
    from easy_profile import EasyProfileMiddleware

    app.wsgi_app = EasyProfileMiddleware(app.wsgi_app)

from src.services import (
    space_owner_service,
    space_service,
    auth_service,
    table_service,
    statistics_service,
)

# TODO: Add the blueprints to the app

api.register_blueprint(space_owner_service.blp)
api.register_blueprint(space_service.blp)
api.register_blueprint(auth_service.blp)
api.register_blueprint(table_service.blp)
api.register_blueprint(statistics_service.blp)


@app.errorhandler(500)
def internal_error_handler(error: Exception):
    Session.rollback()
    abort(500, message="The server has an unexpected error.")


@app.teardown_request
def remove_session(exception: Exception = None):
    Session.remove()


@app.after_request
def creds(response):
    """
    Add credentials to the response
    :param response:
    :return:
    """
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Origin"] = settings.CORS_ORIGINS
    return response


@jwt.user_lookup_loader
def load_current_user(jwt_header: dict, jwt_payload: dict) -> "UserAuthSchema":
    g.current_user = jwt_payload.get("sub")

    return jwt_payload.get("sub")
