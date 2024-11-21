#!/usr/bin/env python3
"""
simple flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    """
    GET method that return
    a dict
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    POST route to get values from form
    create user if it does not exist
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # register user if not exist
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    POST route to validate a user
    and create a session for the user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('sesssion_id', session_id)
        return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    DELETE route to implement logout
    by deleting the session data
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user or not session_id:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """
    GET /profile route: Fetch user profile
    """
    session_id = request.cookies.get('session_id')

    # Check if session_id corresponds to a valid user
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)  # Forbidden if session_id is invalid or user not found

    # Respond with the user's email
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """
    generate a pswd reset token for user
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
