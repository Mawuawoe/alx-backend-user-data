#!/usr/bin/env python3
"""
session based authentication implementation
"""
from flask import request
from typing import TypeVar, List
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    session based authentication implementation
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create_session by associating a session_id
        to a user and adding it to the session
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        get user_id base on the session_id
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = SessionAuth.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """
        retrive current user
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Destroys an authenticated session logout.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
