# routes.py
from flask import Blueprint, request, jsonify
from services.auth_service import authenticate_user, create_user

main_routes = Blueprint('main', __name__)

@main_routes.route('/register', methods=['POST'])
def register():
    # Extract data from request
    username = request.json['username']
    password = request.json['password']
    # Assuming create_user returns True if user creation was successful
    if create_user(username, password):
        return jsonify({'message': 'Registration successful'}), 201
    else:
        return jsonify({'message': 'Registration failed'}), 400

@main_routes.route('/login', methods=['POST'])
def login():
    # Implementation for logging in a user
    username = request.json['username']
    password = request.json['password']
    if authenticate_user(username, password):
        # Assume generate_tokens is a function that returns access and refresh tokens
        tokens = generate_tokens(username)
        return jsonify(tokens), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

