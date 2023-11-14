#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import User, Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method that saves a new user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Method that takes in arbitrary keyword arguments
        and returns the first row found in the users table
        as filtered by the method’s input arguments
        """
        if not kwargs:
            raise InvalidRequestError
        if not all(key in User.__table__.columns for key in kwargs):
            raise InvalidRequestError
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
        except Exception:
            raise InvalidRequestError
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Method that takes as argument a required user_id integer
        and arbitrary keyword arguments, and returns None
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
        return None

    def destroy_user(self, user_id: int) -> None:
        """Method that takes as argument a required user_id integer
        and returns None
        """
        user = self.find_user_by(id=user_id)
        self._session.delete(user)
        self._session.commit()
        return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """Method that takes as argument a session_id string
        and returns the corresponding User or None
        """
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        try:
            user = self._session.query(User).filter_by(
                session_id=session_id).first()
        except Exception:
            return None
        return user

    def get_reset_password_token(self, email: str) -> str:
        """Method that takes an email string argument
        and returns the user’s reset_token
        """
        if not email:
            return None
        if not isinstance(email, str):
            return None
        try:
            user = self._session.query(User).filter_by(email=email).first()
        except Exception:
            raise ValueError
        if not user:
            raise ValueError
        reset_token = user.reset_token
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Method that takes as argument a reset_token string
        and a password string and returns None
        """
        if not reset_token:
            return None
        if not isinstance(reset_token, str):
            return None
        if not password:
            return None
        if not isinstance(password, str):
            return None
        try:
            user = self._session.query(User).filter_by(
                reset_token=reset_token).first()
        except Exception:
            raise ValueError
        if not user:
            raise ValueError
        user.hashed_password = password
        user.reset_token = None
        self._session.commit()
        return None

    def update_session_id(self, user_id: int, session_id: str) -> None:
        """Method that takes as argument a user_id integer
        and a session_id string and returns None
        """
        if not user_id:
            return None
        if not isinstance(user_id, int):
            return None
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        try:
            user = self._session.query(User).filter_by(id=user_id).first()
        except Exception:
            raise ValueError
        if not user:
            raise ValueError
        user.session_id = session_id
        self._session.commit()
        return None
