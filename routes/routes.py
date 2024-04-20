from flask import Blueprint, jsonify, request
from auth import create_user, authenticate_user  # Import the actual implementations

# Creating a Blueprint called 'main_routes'
main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/')
def home():
    return "Welcome to the Pet Store Backend Project!"

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if create_user(username, password):
            return jsonify({'message': 'Registration successful'}), 201
        else:
            return jsonify({'message': 'Registration failed'}), 400
    return "GET request received, but this route expects a POST."

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if authenticate_user(username, password):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    return "GET request received, but this route expects a POST."
