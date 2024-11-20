#!/usr/bin/env python3
"""auth module
"""
from user import Base, User
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    the bcrypt.gensalt() makes this hash unique
    even if two user have same password
    """
    hashpswd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashpswd
