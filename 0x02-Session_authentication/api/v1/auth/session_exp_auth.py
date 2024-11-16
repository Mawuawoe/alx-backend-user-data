#!/usr/bin/env python3
""" Session Expiration Authentication """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Session Expiration Authentication class """

    def __init__(self):
        """ Initialize the session duration """
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a session with an expiration time """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Store session information with created_at
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve the user ID based on the session ID """
        if not session_id or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict or "created_at" not in session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if created_at +\
                timedelta(seconds=self.session_duration) < datetime.now():
            return None  # Session expired

        return session_dict.get("user_id")
