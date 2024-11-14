#!/usr/bin/env python3
"""
module to implement basic Authentication
"""
from flask import request
from typing import TypeVar, List
# from api.v1.auth.auth import Auth
from auth import Auth


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
