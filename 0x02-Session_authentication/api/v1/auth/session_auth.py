#!/usr/bin/env python3
"""
session based authentication implementation
"""
from flask import request
from typing import TypeVar, List
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    session based authentication implementation
    """
    pass
