from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os

class User:
    def __init__(self, username, password, db):
        self.username = username
        self.password = self.hash_password(password)  # Hash password upon initialization
        self.db = db
        self.collection = self.db.users  # Assumes there is a 'users' collection in the MongoDB database

    def hash_password(self, password):
        """Hash a password for storing."""
        return generate_password_hash(password)

    def verify_password(self, password):
        """Check hashed password. Return True if matches, False otherwise."""
        return check_password_hash(self.password, password)

    def save(self):
        """Save the user in the database."""
        user_data = {
            "username": self.username,
            "password": self.password  # Store the hashed password
        }
        if self.collection.find_one({"username": self.username}):
            raise Exception("User already exists")
        return self.collection.insert_one(user_data)

    @classmethod
    def find_by_username(cls, username, db):
        """Query the database for a user by username."""
        user_data = db.users.find_one({"username": username})
        if user_data:
            return cls(username=user_data['username'], password=user_data['password'], db=db)
        else:
            return None

# Usage example (not to be included in the module):
# Connect to MongoDB (adjust the URI as needed)
# mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
# client = MongoClient(mongo_uri)
# db = client.PetStoreProject
# user = User('johndoe', 's3cr3t', db)
# user.save()
# found_user = User.find_by_username('johndoe', db)
# print(found_user.verify_password('s3cr3t'))  # Should return True if the password matches

