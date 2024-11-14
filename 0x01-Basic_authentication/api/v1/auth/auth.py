#!/usr/bin/env python3
"""
module to implement basic Authentication
"""
from flask import request
from typing import TypeVar, List


class Auth():
    """the class to handle basic authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """access required"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path and excluded paths are slash-tolerant
        normalized_path = path if path.endswith('/') else path + '/'

        for ex_path in excluded_paths:
            if ex_path.endswith('/'):
                if normalized_path == ex_path:
                    return False
            else:
                if normalized_path == ex_path + '/':
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieve the Authorization header from the request."""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """the current_user"""
        return None
