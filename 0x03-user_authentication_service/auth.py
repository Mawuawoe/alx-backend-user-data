#!/usr/bin/env python3
"""auth module
"""
from user import Base, User
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    the bcrypt.gensalt() makes this hash unique
    even if two user have same password
    """
    hashpswd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashpswd


def _generate_uuid() -> str:
    """
    generate a uuid
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate a user
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        create session implementation
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        verify user login based on session data
        retrieve user based on session
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroy session by just updating
        user.session_id to None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generate a reset token for user
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_tkn = _generate_uuid()
            user.reset_token = reset_tkn
            return reset_tkn
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update the user password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hash_pswd = _hash_password(password)
            user.hashed_password = hash_pswd
            user.reset_token = None

        except NoResultFound:
            raise ValueError

        return None
