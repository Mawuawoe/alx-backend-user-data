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
        return False

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """the current_user"""
        return None
