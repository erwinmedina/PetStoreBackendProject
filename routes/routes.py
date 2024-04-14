# File: routes/routes.py
from flask import Blueprint, request, jsonify
from services.auth_service import authenticate_user, create_user

main_routes = Blueprint('main', __name__)

@main_routes.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    if create_user(username, password):
        return jsonify({'message': 'Registration successful'}), 201
    else:
        return jsonify({'message': 'Registration failed'}), 400

@main_routes.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    if authenticate_user(username, password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
