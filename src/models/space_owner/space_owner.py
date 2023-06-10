from typing import List, Optional

from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from base.rest_item import RestItem
from base.settings import settings


class SpaceOwner(RestItem):
    """
    SpaceOwner model class
    """
    __tablename__ = 'space_owner'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    spaces: Mapped[List['Space']] = relationship()

    @classmethod
    def verify_google_token(cls, token: str) -> bool:
        """
        Verify if the token is valid for Google.
        :param token: encoded token
        :return: bool whether the token is valid or not
        """
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

            # Get the user's Google Account ID from the decoded token, if the key doesn't exist the process failed.
            return idinfo.get('sub', False)
        except GoogleAuthError:
            # Invalid token
            return False
