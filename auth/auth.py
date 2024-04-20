from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
from models.user import User  # Ensure this model is correctly defined

bcrypt = Bcrypt()
jwt = JWTManager()

def initialize_auth(app):
    # Initialize bcrypt and JWT with the Flask app
    bcrypt.init_app(app)
    jwt.init_app(app)

def create_user(username, password):
    # Hash password and create a new user in the database
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password)
    success = user.save()  # Make sure this method actually persists data to your database
    return success is not None

def authenticate_user(username, password):
    # Check user credentials and return a JWT token if valid
    user = User.find_by_username(username)  # Ensure this query is correctly accessing the user
    if user and bcrypt.check_password_hash(user.password, password):
        # Create a new token with the user id inside
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=7))
        return True, access_token
    return False, None
