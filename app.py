import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_caching import Cache

# Import Blueprints
from routes.routes import main_routes
from routes.user_routes import userapp
from routes.pet_inventory_routes import petapp

def create_app():
    # Load environment variables
    load_dotenv()

    # Create a Flask instance
    app = Flask(__name__)

    # Configure the application with environment variables
    app.config['MONGO_URI'] = os.environ.get('MONGODB_URI')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')
    
    # Configure Redis for caching
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL')

    # Initialize Redis Cache
    cache = Cache(app)

    # Initialize MongoDB
    mongo_client = MongoClient(app.config['MONGO_URI'])
    db = mongo_client["PetStoreProject"]
    collection = db["PetStore"]
    users_collection = db["users"]

    # Initialize Flask extensions: Bcrypt and JWTManager
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    # Register Blueprints for different parts of the application
    app.register_blueprint(main_routes)
    app.register_blueprint(userapp, cache=cache)
    app.register_blueprint(petapp, cache=cache)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
