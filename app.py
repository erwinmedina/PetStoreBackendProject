from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Correct the Blueprint import based on your file and folder structure
from routes.routes import main_routes  # If main_routes is defined in routes/routes.py

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['MONGO_URI'] = "mongodb://localhost:27017/petstore"
    app.config['SECRET_KEY'] = "your_secret_key_here"
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production

    # Initialize MongoDB
    mongo = PyMongo(app)

    # Initialize bcrypt and JWT
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    # Register the Blueprint
    app.register_blueprint(main_routes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
