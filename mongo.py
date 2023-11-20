from logger import Logger

from pymongo import MongoClient

class MongoSoftware:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.movies = self.client["software-2"]["movies"]

        Logger.info("Connected to MongoDB")

    def __del__(self):
        self.client.close()
        Logger.info("Disconnected from MongoDB")
