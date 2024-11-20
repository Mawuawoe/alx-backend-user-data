#!/usr/bin/env python3
"""auth module
"""
from user import Base, User
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    the bcrypt.gensalt() makes this hash unique
    even if two user have same password
    """
    hashpswd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashpswd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        add user
        """
        try:
            # find the user with the given email
            self._db.find_user_by(email=email)
        except NoResultFound:
            # add user to database
            return self._db.add_user(email, _hash_password(password))

        else:
            # if user already exists, throw error
            raise ValueError('User {} already exists'.format(email))
