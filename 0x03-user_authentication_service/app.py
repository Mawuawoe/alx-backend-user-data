#!/usr/bin/env python3
"""
simple flask app
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route('/')
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
