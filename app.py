import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_caching import Cache

# Import your Blueprints
from routes.routes import main_routes
from routes.user_routes import userapp

def create_app():
    # Load environment variables
    load_dotenv()

    # Create a Flask instance
    app = Flask(__name__)

    # Configure the application
    app.config['MONGO_URI'] = os.environ.get('MONGODB_URI')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret')  # Adjust this for production

    # Configure Redis for caching
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')  # Defaulting to local Redis

    # Initialize Cache
    cache = Cache(app)

    # Initialize MongoDB
    mongo_client = MongoClient(app.config['MONGO_URI'])
    db = mongo_client["PetStoreProject"]
    collection = db["PetStore"]
    users_collection = db["users"]

    # Initialize Flask extensions
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    # Register Blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(userapp, url_prefix='/users')

    # Define routes directly in the app for demonstration
    @app.route("/api/petstore", methods=["GET"])
    @cache.cached(timeout=60)  # Caching this route for 60 seconds
    def get_AllPetStore():
        data = list(collection.find({}))
        return jsonify([{'_id': str(item['_id']), **item} for item in data])

    @app.route("/api/petstore/<string:_id>", methods=["GET"])
    @cache.cached(timeout=60)  # Caching this route for 60 seconds
    def get_PetStoreById(_id):
        data = collection.find_one({'_id': ObjectId(_id)})
        if data:
            data['_id'] = str(data['_id'])
            return jsonify(data)
        else:
            return jsonify({"Error": "Item not found"}), 404

    @app.route("/api/petstore", methods=["POST"])
    def add_PetStore():
        data = request.json
        if "name" not in data:
            return jsonify({"Error": "Missing name field"}), 400
        collection.insert_one(data)
        data['_id'] = str(data['_id'])
        cache.clear()  # Clear cache after adding a new item
        return jsonify(data), 201

    @app.route("/api/petstore/<string:_id>", methods=["DELETE"])
    def delete_PetStoreById(_id):
        result = collection.delete_one({'_id': ObjectId(_id)})
        if result.deleted_count:
            cache.clear()  # Clear cache after deleting an item
            return jsonify({"Message": "Item deleted successfully"}), 200
        else:
            return jsonify({"Error": "Item not found"}), 404

    @app.route("/api/petstore/<string:_id>", methods=["PUT"])
    def update_PetStoreById(_id):
        data = request.json
        result = collection.update_one({'_id': ObjectId(_id)}, {"$set": data})
        if result.modified_count:
            cache.clear()  # Clear cache after updating an item
            return jsonify({"Message": "Item updated successfully"}), 200
        else:
            return jsonify({"Error": "Item not found"}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
