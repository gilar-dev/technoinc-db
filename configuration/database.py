from pymongo import MongoClient
from pymongo.server_api import ServerApi
from configuration.config import DB_URL

client = MongoClient(DB_URL, server_api=ServerApi("1"))
db = client["technoinc-db"]