from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")
DATABASE = client.get_database("confessions")
SETUP = DATABASE.get_collection("setup")
CONFESSIONS = DATABASE.get_collection("confessions")