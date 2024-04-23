from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
from models.user import User
import redis
import os
from flask import Blueprint
from pymongo import MongoClient
from dotenv import load_dotenv

# Setup Redis connection
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PASSWORD'), decode_responses=True)

bcrypt = Bcrypt()
jwt = JWTManager()

# Handles loading the database
userapp = Blueprint('userapp', __name__)
load_dotenv()
mongo_uri = os.environ.get('MONGO_URI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client["PetStoreProject"]

def initialize_auth(app):
    # Initialize bcrypt and JWT with the Flask app
    bcrypt.init_app(app)
    jwt.init_app(app)

def create_user(username, password, firstname, lastname, email, streetname, suiteapt, city, state, zipcode):
    
    # Finds the user if it exists
    if User.find_by_username(username, db) is not None:
        print("User already exists")
        return False  # User already exists
    
    # Hash password and create a new user in the database
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    user = User(
        username=username, 
        password=hashed_password, 
        db=db,
        email=email,
        firstname=firstname,
        lastname=lastname,
        streetname=streetname,
        suiteapt=suiteapt,
        city=city,
        state=state,
        zipcode=zipcode
    )
    
    success = user.save()
    if success:
        print("User created successfully")
        return True
    else:
        print("Failed to create user.")
        return False

def authenticate_user(username, password):
    # Check user credentials and return a JWT token if valid
    user = User.find_by_username(username, db)
    
    if not user:
        print("User not found.")
        return False, None
    
    if bcrypt.check_password_hash(user.password, password):
        # Create a new token with the user id inside
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=7))

        # Cache the JWT token in Redis
        redis_client.setex(f"user_token:{username}", timedelta(days=7), access_token)
        return True, access_token
    
    return False, None
