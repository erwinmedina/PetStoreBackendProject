
from flask import Blueprint, jsonify, request
from auth import create_user, authenticate_user  # Ensure these are correctly implemented

# Creating a Blueprint called 'main_routes'
main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    return "Welcome to the Pet Store Backend Project!"

@main_routes.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Extract username and password from the JSON body of the request
        username = request.json.get('username')
        password = request.json.get('password')
        # Attempt to create a new user
        if create_user(username, password):
            return jsonify({'message': 'Registration successful'}), 201
        else:
            return jsonify({'message': 'Registration failed'}), 400
    elif request.method == 'GET':
        return "This endpoint is for registering users. Send a POST request with 'username' and 'password' in the JSON body."

@main_routes.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Extract username and password from the JSON body of the request
        username = request.json.get('username')
        password = request.json.get('password')
        # Authenticate the user
        authenticated, token = authenticate_user(username, password)
        if authenticated:
            return jsonify({'message': 'Login successful', 'access_token': token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    elif request.method == 'GET':
        return "This endpoint is for user login. Send a POST request with 'username' and 'password' in the JSON body."
