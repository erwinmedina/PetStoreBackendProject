import os
from dotenv import load_dotenv
from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Load environment variables
load_dotenv()
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/petstore')
mongo_client = MongoClient(mongo_uri)
db = mongo_client["PetStoreProject"]
collection = db["PetStore"]

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')

# Initialize bcrypt and JWT
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Import routes after initialization to avoid circular imports
from routes.routes import main_routes
app.register_blueprint(main_routes)

# API Routes
@app.route("/api/petstore", methods=["GET"])
def get_all_petstore():
    try:
        data = list(collection.find({}))
        for item in data:
            item["_id"] = str(item["_id"])
        return jsonify(data)
    except Exception as e:
        return jsonify({"Error": "Error occurred while retrieving data from database"}), 500

@app.route("/api/petstore/<string:_id>", methods=["GET", "DELETE", "PUT"])
def handle_petstore(_id):
    try:
        obj_id = ObjectId(_id)
    except Exception as e:
        return jsonify({"Error": "Invalid id format"}), 400

    if request.method == 'GET':
        data = collection.find_one({'_id': obj_id})
        if data:
            data["_id"] = str(data["_id"])
            return jsonify(data)
        else:
            return jsonify({"Error": "Item not found"}), 404

    elif request.method == 'DELETE':
        result = collection.delete_one({"_id": obj_id})
        if result.deleted_count == 1:
            return jsonify({"Message": "Item deleted successfully"}), 200
        else:
            return jsonify({"Error": "Item not found"}), 404

    elif request.method == 'PUT':
        data = request.json
        if not data:
            return jsonify({"Error": "No data provided"}), 400
        update_result = collection.update_one({"_id": obj_id}, {"$set": data})
        if update_result.modified_count == 1:
            return jsonify({"Message": "Item updated successfully"}), 200
        else:
            return jsonify({"Error": "Item not found"}), 404

@app.route("/api/petstore", methods=["POST"])
def add_petstore():
    data = request.json
    if not data:
        return jsonify({"Error": "No data provided"}), 400
    result = collection.insert_one(data)
    if result.inserted_id:
        return jsonify({'Message': "Item added successfully", "_id": str(result.inserted_id)}), 201
    else:
        return jsonify({"Error": "Failed to add item"}), 500

def create_app():
    # Place for further app setup if needed
    return app

if __name__ == '__main__':
    create_app().run(debug=True)

