from flask import Flask
from routes import setup_routes

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = "your_mongo_db_uri_here"  # Connect to MongoDB
    app.config['SECRET_KEY'] = "your_secret_key"        # Necessary for session management and JWT

    setup_routes(app)  # Set up all your routes

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
