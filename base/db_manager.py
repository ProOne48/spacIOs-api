from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from base.settings import settings

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy.engine import Engine


def get_db_string(db_name: str = None) -> str:
    """
    Returns the database connection string

    :param db_name: The custom database name. Leave empty to use default connection.
    :return: The database connection string
    """
    db_name = db_name or settings.DB_NAME
    conn_str = f"{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{db_name}"

    return f"postgresql+psycopg2://{conn_str}"


def create_aps_engine(db_name: str = None) -> 'Engine':
    """
    Returns a SQLAlchemy engine with the configuration from settings.py
    :param db_name: The custom database name. Leave empty to use default connection.
    :return: the created engine
    """
    return create_engine(get_db_string(db_name), echo=settings.DEBUG_SQL >= 2, future=True)


Session = scoped_session(sessionmaker(bind=create_aps_engine()))
