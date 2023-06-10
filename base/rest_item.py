from typing import TypeVar, TYPE_CHECKING, Type, Optional, List, Dict

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import DeclarativeBase

from base.db_manager import Session

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy.orm import Query


class BaseSQL(DeclarativeBase):
    """
    Base class for all SQLAlchemy models
    """
    query = Session.query_property()
    session = Session


RestItemSubClass = TypeVar('RestItemSubClass', bound='RestItem')


class RestItem(BaseSQL):

    """
    Base class for all REST items

    Where all CRUDL methods for REST items are defined
    """
    __abstract__ = True
    """
    Query object for running select queries
    """
    query: 'Query'

    """
    Session object for running insert, update and delete queries
    """
    session: Session

    @classmethod
    def find(cls: Type[RestItemSubClass], item_id: int) -> Optional[RestItemSubClass]:
        """
        Finds an item by its id

        :param item_id: the item id
        :return: the item if found, None otherwise
        """
        return cls.session.get(cls, item_id)

    @classmethod
    def find_by(cls: Type[RestItemSubClass], criteria: List = None) -> Optional[RestItemSubClass]:
        """
        Finds the first item matching the criteria
        :param criteria: criteria to find the item
        :return: an instance of the class matching the criteria
        """
        return cls.session.scalars(
            select(cls).where(*criteria)
        ).first()

    @classmethod
    def list(cls, criteria: List = None) -> (List[RestItemSubClass], int):
        """
        Returns a list of items matching the criteria

        :param criteria: criteria to find the items
        :return: a list of items matching the criteria
        """
        query = cls.query
        if criteria is not None:
            query = query.where(*criteria)

        items = query.all()

        return items, len(items)

    def update(self: RestItemSubClass, data: Dict[str, any] = None):
        """
        Updates the current object in the database. If `data` is not None then it will assign each value of data in its
        respective object property (only if the key exists in the data model).
        :param data: a dict with the keys to update and it's values
        :return:
        """
        if data:
            self.add_from_dict(data)
            
        self.commit()
        
    def insert(self: RestItemSubClass):
        """
        Inserts the current object in the database
        :return:
        """
        self.session.add(self)
        self.commit()
        
    def delete(self: RestItemSubClass):
        """
        Deletes the current object from the database
        :return:
        """
        self.session.delete(self)
        self.commit()

    def add_from_dict(self: RestItemSubClass, data: Dict[str, any]):
        """
        Set the properties of the object from a dict
        :param data: a dict with the keys to update and it's values
        :return:
        """
        for field, value in data.items():
            if hasattr(self, field):
                setattr(self, field, value)
                
    def commit(self: RestItemSubClass):
        """
        Commits the current session
        :return:
        """
        try:
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
