from pymongo import MongoClient
from pymongo.server_api import ServerApi
from configuration.config import DB_URI
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(DB_URI, server_api=ServerApi("1"))
db = client["technoinc-db"]