import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from bson import ObjectId

# Correct the Blueprint import based on your file and folder structure
from routes.routes import main_routes  # If main_routes is defined in routes/routes.py

# Handles .env file read.
load_dotenv()
mongo_uri = os.environ.get('MONGODB_URI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client["PetStoreProject"]
collection = db["PetStore"]
app = Flask(__name__)

# ***************************************** #
# Gets all items in the petstore collection #
# ***************************************** #
@app.route("/api/petstore", methods=["GET"])
def get_AllPetStore():
    try:
        data = list(collection.find({}))
        for item in data:
            item["_id"] = str(item["_id"])
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"Error": "Error occurred while retrieving data from database"}), 500

# ********************************************** #
# Gets 1 item by id from the petstore collection #
# ********************************************** #
@app.route("/api/petstore/<string:_id>", methods=["GET"])
def get_PetStoreById(_id):
    try:
        data = collection.find_one({'_id': ObjectId(_id)})
        data["_id"] = str(data["_id"])
        return jsonify(data)
    except Exception as e:
        return jsonify({"Error": "Error occurred while retrieving item from database"}), 500

# ******************************************* #
# Inserts 1 item into the petstore collection #
# ******************************************* #
@app.route("/api/petstore", methods=["POST"])
def add_PetStore():
    try:
        data = request.json
        
        if "Test" not in data:
            return jsonify({"Error": "Test is a required field."}), 400

        collection.insert_one(data)
        return jsonify({'Message': "Item added successfully"}), 201
    except Exception as e:
        print(e)
        return jsonify({"Error": "Error occurred while inserting"}), 500

# *********************************************** #
# Inserts many items into the petstore collection #
# *********************************************** #
@app.route("/api/petstore/bulk", methods=["POST"])
def add_PetStoreBulk():
    try:
        data = request.json
        if not data:
            return jsonify({"Error": "No data was provided in the request"}), 400
        collection.insert_many(data)
        return jsonify({"Message": "Bulk insertion successful"}), 201
    except Exception as e:
        print(e)
        return jsonify({"Error": "Failed to bulk insert items"})

# ************************************************* #
# Deletes 1 item from the petstore collection by ID #
# ************************************************* #
@app.route("/api/petstore/<string:_id>", methods=["DELETE"])
def delete_PetStoreById(_id):
    # Converts to objectid before deleting 
    try:
        obj_id = ObjectId(_id)
    except Exception as e:
        print(e)
        return jsonify({"Error": "Invalid id format"}), 400
    
    # Deletes by id
    delete_result = collection.delete_one({"_id": obj_id})
    if delete_result.deleted_count == 1:
        return jsonify({"Message": "Item deleted successfully"}), 200
    else:
        return jsonify({"Error": "Item not found"}), 404

# ************************************************* #
# Updates 1 item from the petstore collection by ID #
# ************************************************* #
@app.route("/api/petstore/<string:_id>", methods=["PUT"])
def update_PetStoreById(_id):

    # Converts to objectid before updating.
    try:
        obj_id = ObjectId(_id)
    except Exception as e:
        print(e)
        return jsonify({"Error": "Invalid id format"}), 400

    # Checks if there is data
    data = request.json
    if not data:
        return jsonify({"Error": "No data was provided in the request"}), 400
    
    # Updates by id
    update_result = collection.update_one({"_id": obj_id}, {"$set": data})
    if update_result.modified_count == 1:
        return jsonify({"Message": "Item updated successfully"}), 200
    else:
        return jsonify({"Error": "Item not found"}), 404


def create_app():


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
