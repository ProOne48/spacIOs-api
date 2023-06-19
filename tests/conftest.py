import pytest
from sqlalchemy.orm import sessionmaker

from base.rest_item import BaseSQL
from base.settings import settings
from sqlalchemy import create_engine, DDL, MetaData
from base.db_manager import get_db_string
from flask_jwt_extended import create_access_token

from src.app import app as flask_app

from src.models.space_owner import SpaceOwner
from src.models.space import Space

engine = create_engine(get_db_string())
Session = sessionmaker()


def set_database():
    root_engine = create_engine(get_db_string().replace(f'/{settings.DB_NAME}', ''), isolation_level='AUTOCOMMIT')
    root_engine.connect().execute(DDL(f'DROP DATABASE IF EXISTS {settings.DB_NAME};'))
    root_engine.connect().execute(DDL(f'CREATE DATABASE {settings.DB_NAME};'))

    return root_engine


def clean_database(root_engine):
    root_engine.connect().execute(DDL(f'REVOKE CONNECT ON DATABASE {settings.DB_NAME} FROM public;'))
    root_engine.connect().execute(
        DDL(
            f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity "  # noqa S608
            f"WHERE pg_stat_activity.datname = '{settings.DB_NAME}';"
        )
    )
    root_engine.connect().execute(DDL(f'DROP DATABASE {settings.DB_NAME};'))


@pytest.fixture(scope='session')
def connection():
    if settings.ENV_FOR_DYNACONF != 'test':
        raise ValueError({
            'message': 'You must be in test environment to run the tests',
            'current_env': settings.ENV_FOR_DYNACONF
        })

    root_engine = set_database()
    metadata_obj = MetaData()
    metadata_obj.create_all(root_engine)

    connection = engine.connect()
    yield connection

    clean_database(root_engine)
    connection.close()


@pytest.fixture(scope='session', autouse=True)
def setup_db(connection):
    def commit():
        BaseSQL.session.flush()
        BaseSQL.session.expire_all()

    BaseSQL.metadata.bind = connection
    BaseSQL.session.commit = commit

    BaseSQL.metadata.create_all(engine)
    BaseSQL.session.commit()
    yield

    BaseSQL.session.remove()

    pass


@pytest.fixture(autouse=True)
def reset_db():
    BaseSQL.session.rollback()


@pytest.fixture()
def app():
    return flask_app


@pytest.fixture()
def cookie_jwt_auth_header(insert_space_owner):
    flask_app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    token = create_access_token(identity=insert_space_owner.to_auth_data())
    return flask_app.config.get('JWT_ACCESS_COOKIE_NAME'), token


@pytest.fixture()
def space_owner_data():
    return {
        'id': 110,
        'name': 'Space Owner',
        'email': 'space_owner@space_owner.com',
        'spaces': []
    }


@pytest.fixture()
def space_owner_data_with_spaces(space_demo):
    return {
        'id': 110,
        'name': 'Space Owner',
        'email': 'space_owner@space_owner.com',
        'spaces': [space_demo],
    }


@pytest.fixture()
def space_owner_demo(space_owner_data):
    space_owner = SpaceOwner()
    space_owner.add_from_dict(space_owner_data)

    return space_owner


@pytest.fixture()
def space_owner_demo_with_space(space_owner_data_with_spaces):
    space_owner = SpaceOwner()
    space_owner.add_from_dict(space_owner_data_with_spaces)

    return space_owner


@pytest.fixture()
def insert_space_owner(space_owner_demo):

    space_owner_demo.insert()

    return space_owner_demo


@pytest.fixture()
def insert_space_owner_with_spaces(space_owner_demo_with_space):

    space_owner_demo_with_space.insert()

    return space_owner_demo_with_space


@pytest.fixture()
def space_data():
    return {
        'id': 150,
        'name': 'Test Space',
        'max_capacity': 10,
        'space_owner_id': 110,
    }


@pytest.fixture()
def space_demo(space_data):
    space = Space()
    space.add_from_dict(space_data)

    return space


@pytest.fixture()
def another_space_demo(space_data):
    space_data['id'] = 151
    space_data['name'] = 'Another Test Space'
    space = Space()
    space.add_from_dict(space_data)

    return space


@pytest.fixture()
def insert_space(space_demo):
    space_demo.insert()

    return space_demo
