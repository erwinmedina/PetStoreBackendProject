import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, Blueprint, current_app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId
from models.pet_inventory import Pet


petapp = Blueprint('petapp', __name__)
load_dotenv()
mongo_client = MongoClient(os.environ.get("MONGODB_URI"))
db = mongo_client["PetStoreProject"]
pets_collection = db["pets"]


# ***************************************** #
# Get all items in the pets collection      #
# ***************************************** #
@petapp.route("/api/petstore/pets", methods=["GET"])
@jwt_required()
def get_AllPets():
    cache_dict = current_app.extensions["cache"]
    cache = list(cache_dict.values())[0]
    cached_data = cache.get("all_pets_data")

    if cached_data:
        return jsonify(cached_data)
    else:
        try:
            data = list(pets_collection.find({}))
            if len(data) == 0:
                return jsonify({"Error": "No items found"}), 404
            for item in data:
                item['_id'] = str(item['_id'])
            cache.set("all_pets_data", data, timeout=60)
            return jsonify(data)
        
        except Exception as e:
            print(e)
            return jsonify({"Error": "Error occurred while retrieving data from database"}), 500


# ********************************************** #
# Insert 1 item into the pets collection         #
# ********************************************** #
@petapp.route("/api/petstore/pets", methods=["POST"])
@jwt_required()
def add_Pet():
    try:
        data = request.json
        if not all(key in data for key in ['name', 'type', 'weight', 'gender', 'color', 'age']):
            return jsonify({"Error": "Missing required fields"}), 400
        pet = Pet(data['name'], data['type'], data['weight'], data['gender'], data['color'], data['age'], db)
        answer = pet.save()
        if answer['acknowledged']:
            return jsonify({"Message": "Pet added successfully"}), 201
        else:
            return jsonify({"Error": "Pet already exists"}), 403
    except Exception as e:
        print(e)
        return jsonify({"Error": "Error occurred while inserting"}), 500
    
    
# ******************************************** #
# Delete 1 item from the pet collection by ID  #
# ******************************************** #
@petapp.route("/api/petstore/pets/<string:_id>", methods=["DELETE"])
@jwt_required()
def delete_PetById(_id):
    try :
        result = pets_collection.delete_one({"_id": ObjectId(_id)})
        if result.deleted_count:
            return jsonify({"Message": "Pet deleted successfully"}), 200
        else:
            return jsonify({"Error": "Pet not found"}), 404
    except Exception as e:
        return jsonify({"Error": "Error occurred while deleting"}), 500
    

# ************************************************* #
# Delete 1 item from the pet collection by name     #
# ************************************************* #
@petapp.route("/api/petstore/pets/name/<string:name>", methods=["DELETE"])
@jwt_required()
def delete_PetByName(name):
    try :
        filter = {'petname': name}
        result = pets_collection.find_one_and_delete(filter, projection = None, sort = None)
        if result is not None:
            return jsonify({"Message": "Pet deleted successfully"}), 200
        else:
            return jsonify({"Error": "Pet not found"}), 404
    except Exception as e:
        return jsonify({"Error": "Error occurred while deleting"}), 500

# ************************************************ #
# Update pets weight from the pet collection  #
# ************************************************ #
@petapp.route("/api/petstore/pets/weight", methods=["PUT"])
@jwt_required()
def update_Pet_weight():
    try:
        data = request.json
        if not all(key in data for key in ["petname", "petweight"]):
            return jsonify({"Error": "Missing required fields"}), 400

        result = pets_collection.find_one_and_update(
            {"petname": data["petname"]}, {"$set": data}
        )
        if result is not None:
            return jsonify({"Message": "Pet updated successfully"}), 200
        else:
            return jsonify({"Error": "Pet not found"}), 404
    except Exception as e:
        return jsonify({"Error": "Error occurred while updating"}), 500

# ************************************************ #
# Update pets age from the pet collection  #
# ************************************************ #
@petapp.route("/api/petstore/pets/age", methods=["PUT"])
@jwt_required()
def update_Pets_Age():
    try:
        data = request.json
        if not all(key in data for key in ["petname", "petage"]):
            return jsonify({"Error": "Missing required fields"}), 400

        result = pets_collection.find_one_and_update(
            {"petname": data["petname"]}, {"$set": data}
        )
        if result is not None:
            return jsonify({"Message": "Pet updated successfully"}), 200
        else:
            return jsonify({"Error": "Pet not found"}), 404
    except Exception as e:
        return jsonify({"Error": "Error occurred while updating"}), 500