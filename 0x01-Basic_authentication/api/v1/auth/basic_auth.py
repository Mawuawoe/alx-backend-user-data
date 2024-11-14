#!/usr/bin/env python3
"""
module to implement basic Authentication
"""
from flask import request
from typing import TypeVar, List
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """
    class to implement basic Authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        to extract the Base64 encoded string
        for basic authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """
        decode from base64 to str
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Encode to bytes, decode from Base64, and
            # then decode to a UTF-8 string
            encoded_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(encoded_bytes)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            # Return None if the input is not valid Base64
            # or if UTF-8 decoding fails
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> (str, str):
        """
        Extracts user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        # Split once to handle cases where password might contain ":"
        user_email, pswd = decoded_base64_authorization_header.split(':', 1)
        return user_email, pswd

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieves a user based on the user's authentication credentials.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None
