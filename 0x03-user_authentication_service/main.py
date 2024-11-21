#!/usr/bin/env python3
"""
Test module for the Flask application
"""
import requests


BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Test user registration."""
    response = requests.post(f"{BASE_URL}/users",
                             data={"email": email, "password": password})
    assert response.status_code == 200,\
        f"Failed to register user: {response.text}"
    payload = response.json()
    assert payload == {"email": email,
                       "message": "user created"},\
        f"Unexpected response: {payload}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with incorrect password."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 401,\
        f"Expected 401, got {response.status_code}"


def log_in(email: str, password: str) -> str:
    """Test login with correct credentials."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 200, f"Failed to log in: {response.text}"
    payload = response.json()
    assert "session_id" in response.cookies,\
        "No session_id in response cookies"
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """Test accessing profile without logging in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403,\
        f"Expected 403, got {response.status_code}"


def profile_logged(session_id: str) -> None:
    """Test accessing profile while logged in."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200,\
        f"Failed to access profile: {response.text}"
    payload = response.json()
    assert "email" in payload, f"Unexpected response: {payload}"


def log_out(session_id: str) -> None:
    """Test logging out."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, f"Failed to log out: {response.text}"


def reset_password_token(email: str) -> str:
    """Test getting a reset password token."""
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={"email": email})
    assert response.status_code == 200,\
        f"Failed to get reset token: {response.text}"
    payload = response.json()
    assert "reset_token" in payload, f"Unexpected response: {payload}"
    return payload["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating the password."""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email,
              "reset_token": reset_token,
              "new_password": new_password},
    )
    assert response.status_code == 200,\
        f"Failed to update password: {response.text}"
    payload = response.json()
    assert payload == {"email": email,
                       "message": "Password updated"},\
        f"Unexpected response: {payload}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
