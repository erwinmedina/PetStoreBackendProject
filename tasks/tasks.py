from celery import Celery
from pymongo import MongoClient
import os

app = Celery('tasks', broker="amqp://127.0.0.1:5672")

@app.task()
def save_pet_to_db(pet_data):
    mongo_client = MongoClient(os.environ.get("MONGODB_URI"))
    db = mongo_client['PetStoreProject']
    collection = db["pets"]
    collection.insert_one(pet_data)
    return {"acknowledged": True}