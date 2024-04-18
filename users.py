import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, Blueprint
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from bson import ObjectId

userapp = Blueprint('userapp', __name__)
mongo_uri = os.environ.get('MONGODB_URI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client["PetStoreProject"]
users_collection = db["users"]


# ***************************************** #
# Gets all items in the users collection #
# ***************************************** #
@userapp.route("/api/petstore/users", methods=["GET"])
def get_AllUsers():
    try:
        data = list(users_collection.find({}))
        for item in data:
            item["_id"] = str(item["_id"])
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"Error": "Error occurred while retrieving data from database"}), 500


# ********************************************** #
# Get a specific user from the collection #
# ********************************************** #
@userapp.route("/api/petstore/users/<string:_id>", methods=["GET"])
def get_UserById(_id):
    try:
        data = users_collection.find_one({'_id': ObjectId(_id)})
        data["_id"] = str(data["_id"])
        return jsonify(data)
    except Exception as e:
        return jsonify({"Error": "Error occurred while retrieving item from database"}), 500


# ******************************************* #
# Inserts 1 item into the users collection    #
# ******************************************* #
@userapp.route("/api/petstore/users", methods=["POST"])
def add_User():
    try:
        data = request.json

        # check if request has the required fields
        if 'Address' not in data: 
            return jsonify({
                'error': 'Missing Address',
                "required": "Address"
                }), 400

        if 'StreetName' not in data['Address']:
            return jsonify({
                'error': 'Missing Street Name',
                "required": "Street Name"
                }), 400
        
        if 'City' not in data['Address']: 
            return jsonify({
                'error': 'Missing City',
                "required": "City"
                }), 400
        
        if 'State' not in data['Address']:
            return jsonify({
                'error': 'Missing State',
                "required": "State"
                }), 400
        
        if 'Zipcode' not in data['Address']:
            return jsonify({
                'error': 'Missing ZipCode',
                "required": "Zipcode"
                }), 400
        
        if 'FirstName' not in data:
            return jsonify({
                'error': 'Missing FirstName',
                "required": "FirstName"
                }), 400
        
        if 'LastName' not in data:
            return jsonify({
                'error': 'Missing LastName',
                "required": "LastName"
                }), 400
        
        if 'Email' not in data:
            return jsonify({
                'error': 'Missing Email',
                "required": "Email"
                }), 400
        
        if 'Password' not in data:
            return jsonify({
                'error': 'Missing Password',
                "required": "Password"
                }), 400

        # This field is not required so if it not present it will be 
        # set to an empty string
        if 'Suite&Apt' not in data['Address']:
            data['Address']['Suite&Apt'] = ""

        #Checking for existing email address
        document = users_collection.find({"Email": email})
        data = list(document)
        if len(data) > 0:
            return jsonify({"Error": "User already exists"}), 400

        users_collection.insert_one(data)
        return jsonify({"Message": "Item added successfully"}), 201
    except Exception as e:
        print(e)
        return jsonify({"Error": "Error occurred while inserting"}), 500


# *********************************************** #
# Delete 1 item from the users collection by ID   #
# *********************************************** #
@userapp.route("/api/petstore/users/<string:_id>", methods=["DELETE"])
def delete_UserById(_id):
    # Converts to objectid before deleting 
    try:
        obj_id = ObjectId(_id)
    except Exception as e:
        print(e)
        return jsonify({"Error": "Invalid id format"}), 400
    
    # Deletes by id
    delete_result = users_collection.delete_one({"_id": obj_id})
    if delete_result.deleted_count == 1:
        return jsonify({"Message": "Item deleted successfully"}), 200
    else:
        return jsonify({"Error": "Item not found"}), 404


# ************************************************* #
# Delete 1 item from the users collection by email  #
# ************************************************* #
@userapp.route("/api/petstore/users/email/<string:email>", methods=["DELETE"])
def delete_UserByEmail(email):
    try:
        document = users_collection.find({"Email": email})
        data = list(document)
        if len(data) == 0:
            return jsonify({"Error": "Item not found"}), 404
        else:
            obj_id = data[0]["_id"]
            users_collection.delete_one({"_id": obj_id})  
            return jsonify({"Message": "Item deleted successfully"}), 200
        
    except Exception as e:
        return jsonify({"Error": "Error occurred while retrieving item from database"}), 500