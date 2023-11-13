#!/usr/bin/env python3
""" User module
"""
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


class User(declarative_base()):
    """ User class
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

