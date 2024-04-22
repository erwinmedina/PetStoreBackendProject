
from flask import Blueprint, jsonify, request
from auth import create_user, authenticate_user
from dotenv import load_dotenv
from pymongo import MongoClient
import os

# Create a Blueprint for main routes
main_routes = Blueprint('main_routes', __name__)
userapp = Blueprint('userapp', __name__)
load_dotenv()
mongo_uri = os.environ.get('MONGODB_URI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client["PetStoreProject"]
users_collection = db["users"]


@main_routes.route('/')
def home():
    return "Welcome to the Pet Store Backend Project!"

@main_routes.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if create_user(username, password):
            return jsonify({'message': 'Registration successful'}), 201
        else:
            return jsonify({'message': 'Registration failed'}), 400
    elif request.method == 'GET':
        return "This endpoint is for registering users. Send a POST request with 'username' and 'password'."

@main_routes.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        authenticated, token = authenticate_user(username, password)
        if authenticated:
            return jsonify({'message': 'Login successful', 'access_token': token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    elif request.method == 'GET':
        return "This endpoint is for user login. Send a POST request with 'username' and 'password'."
