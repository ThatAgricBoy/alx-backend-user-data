#!/usr/bin/env python3
"""returns the _hash_ of a password."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """_summary_

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """_summary_

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """
    id = uuid4()
    return str(id)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            User: _description_
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            bool: _description_
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """_summary_

        Args:
            email (str): _description_

        Returns:
            str: _description_
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """_summary_

        Args:
            session_id (str): _description_

        Returns:
            str: _description_
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """_summary_

        Args:
            user_id (int): _description_
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None
