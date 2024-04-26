from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os


class Pet:
    def __init__(self, petname, pettype, petweight, petgender, petcolor, petage, db):
        self.petname = petname
        self.pettype = pettype
        self.petweight = petweight
        self.petgender = petgender
        self.petcolor = petcolor
        self.petage = petage
        self.db = db
        self.collection = self.db.pets

    def save(self):
        """Save the pet in the database."""
        pet_data = {
            "petname": self.petname,
            "pettype": self.pettype,
            "petweight": self.petweight,
            "petgender": self.petgender,
            "petcolor": self.petcolor,
            "petage": self.petage
        }
        if self.collection.find_one({"petname": self.petname}):
            return {"acknowledged": False}
        self.collection.insert_one(pet_data)
        return {"acknowledged": True}
    
    @classmethod
    def find_by_petname(cls, petname, db):
        """Query the database for a pet by petname."""
        pet_data = db.pets.find_one({"petname": petname})
        if pet_data:
            return cls(petname=pet_data['petname'], pettype=pet_data['pettype'], petweight=pet_data['petweight'], petgender=pet_data['petgender'], petcolor=pet_data['petcolor'], db=db)
        else:
            return None