import os
from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

# Correct the Blueprint import based on your file and folder structure
from routes.routes import main_routes  # If main_routes is defined in routes/routes.py

def create_app():

    # Handles .env file read.
    load_dotenv()
    mongo_uri = os.environ.get('MONGODB_URI')
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client["PetStoreProject"]
    collection = db["PetStore"]

    app = Flask(__name__)

    # Configuration
    # app.config['MONGO_URI'] = mongo_uri
    # app.config['SECRET_KEY'] = "your_secret_key_here"
    # app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production

    # Initialize MongoDB
    data = collection.find_one()
    print(data)

    # Initialize bcrypt and JWT
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    # Register the Blueprint
    app.register_blueprint(main_routes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
