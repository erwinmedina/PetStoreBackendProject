from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
from models.user import User
import redis
import os

# Setup Redis connection
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PASSWORD'), decode_responses=True)

bcrypt = Bcrypt()
jwt = JWTManager()

def initialize_auth(app):
    # Initialize bcrypt and JWT with the Flask app
    bcrypt.init_app(app)
    jwt.init_app(app)

def create_user(username, password):
    # Hash password and create a new user in the database
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    if User.find_by_username(username) is not None:
        return False, "User already exists"  # User already exists
    user = User(username=username, password=hashed_password)
    success = user.save()
    if success:
        return True, "User created successfully"
    else:
        return False, "Failed to create user"

def authenticate_user(username, password):
    # Check user credentials and return a JWT token if valid
    user = User.find_by_username(username)
    if not user:
        return False, "User not found", None
    if bcrypt.check_password_hash(user.password, password):
        # Create a new token with the user id inside
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=7))
        # Cache the JWT token in Redis
        redis_client.setex(f"user_token:{username}", timedelta(days=7), access_token)
        return True, "Authentication successful", access_token
    return False, "Invalid credentials", None
