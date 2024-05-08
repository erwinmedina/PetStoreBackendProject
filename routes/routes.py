
from flask import Blueprint, jsonify, request, current_app  
from auth import create_user, authenticate_user

# Create a Blueprint for main routes
main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    current_app.logger.debug(f"Server host: {request.host}")
    return "Welcome to the Pet Store Backend Project!"

@main_routes.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.json
        if "username" not in data:
            return jsonify({'message': 'Username is missing'}), 400
        
        if "password" not in data:
            return jsonify({'message': 'Password is missing'}), 400
        
        if "firstname" not in data:
            return jsonify({'message': 'Firstname is missing'}), 400
        
        if "lastname" not in data:
            return jsonify({'message': 'Lastname is missing'}), 400
        
        if "email" not in data:
            return jsonify({'message': 'Email is missing'}), 400
        
        if "address" not in data:
            return jsonify({'message': 'Address is missing'}), 400
        
        if "streetname" not in data['address']:
            return jsonify({'message': 'Streetname is missing'}), 400
        
        if "city" not in data['address']:
            return jsonify({'message': 'City is missing'}), 400
        
        if "state" not in data['address']:
            return jsonify({'message': 'State is missing'}), 400
        
        if "zipcode" not in data['address']:
            return jsonify({'message': 'Zipcode is missing'}), 400
        
        if "suite&apt" not in data['address']:
            return jsonify({'message': 'Suite&apt is missing'}), 400
        
        username = request.json.get('username')
        firstname = request.json.get('firstname')
        lastname = request.json.get('lastname')
        email = request.json.get('email')
        password = request.json.get('password')

        address = request.json.get('address', {})
        streetname = address.get('streetname')
        suiteapt = address.get('suite&apt')
        city = address.get('city')
        state = address.get('state')
        zipcode = address.get('zipcode')

        if create_user(username, password, firstname, lastname, email, streetname, suiteapt, city, state, zipcode):
            return jsonify({'message': 'Registration successful'}), 201
        else:
            return jsonify({'message': 'Registration failed'}), 400
    elif request.method == 'GET':
        return "This endpoint is for registering users. Send a POST request with 'username' and 'password'."

@main_routes.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.json
        if not all(k in data for k in ("username","password")):
            return jsonify({'message': "missing credentials"}), 400
        username = request.json.get('username')
        password = request.json.get('password')
        authenticated, token = authenticate_user(username, password)
        if authenticated:
            return jsonify({'message': 'Login successful', 'access_token': token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    elif request.method == 'GET':
        return "This endpoint is for user login. Send a POST request with 'username' and 'password'."
