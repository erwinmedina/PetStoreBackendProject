import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, Blueprint
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId


userapp = Blueprint('userapp', __name__)
load_dotenv()
mongo_uri = os.environ.get('MONGODB_URI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client["PetStoreProject"]
users_collection = db["users"]

# ***************************************** #
# Gets all items in the users collection    #
# ***************************************** #
@userapp.route("/api/petstore/users", methods=["GET"])
@jwt_required()
def get_AllUsers():
    try:
        data = list(users_collection.find({}))
        return jsonify([{'_id': str(item['_id']), **item} for item in data])
    except Exception as e:
        print(e)
        return jsonify({"Error": "Error occurred while retrieving data from database"}), 500

# ********************************************** #
# Get a specific user from the collection        #
# ********************************************** #
@userapp.route("/api/petstore/users/<string:_id>", methods=["GET"])
@jwt_required()
def get_UserById(_id):
    try:
        data = users_collection.find_one({'_id': ObjectId(_id)})
        if data:
            data['_id'] = str(data['_id'])
            return jsonify(data)
        else:
            return jsonify({"Error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"Error": "Error occurred while retrieving item from database"}), 500

# ******************************************* #
# Inserts 1 item into the users collection    #
# ******************************************* #
@userapp.route("/api/petstore/users", methods=["POST"])
def add_User():
    try:
        data = request.json
        if not all(key in data for key in ['FirstName', 'LastName', 'Email', 'Password']):
            return jsonify({"Error": "Missing required fields"}), 400
        if users_collection.find_one({"Email": data['Email']}):
            return jsonify({"Error": "User already exists"}), 409
        data['Password'] = Bcrypt().generate_password_hash(data['Password']).decode('utf-8')
        users_collection.insert_one(data)
        return jsonify({"Message": "User added successfully", "_id": str(data['_id'])}), 201
    except Exception as e:
        print(e)
        return jsonify({"Error": "Error occurred while inserting"}), 500

# *********************************************** #
# Delete 1 item from the users collection by ID   #
# *********************************************** #
@userapp.route("/api/petstore/users/<string:_id>", methods=["DELETE"])
@jwt_required()
def delete_UserById(_id):
    try :
        result = users_collection.delete_one({'_id': ObjectId(_id)})
        if result.deleted_count:
            return jsonify({"Message": "User deleted successfully"}), 200
        else:
            return jsonify({"Error": "User not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"Error": "Error occurred while deleting"}), 500

# ************************************************* #
# Delete 1 item from the users collection by email  #
# ************************************************* #
@userapp.route("/api/petstore/users/email/<string:email>", methods=["DELETE"])
@jwt_required()
def delete_UserByEmail(email):
    try :
        result = users_collection.delete_one({"Email": email})
        if result.deleted_count:
            return jsonify({"Message": "User deleted successfully"}), 200
        else:
            return jsonify({"Error": "User not found"}), 404
    except Exception as e:
        return jsonify({"Error": "Error occurred while deleting"}), 500
