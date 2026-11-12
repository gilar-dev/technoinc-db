from pymongo.server_api import ServerApi
from pymongo import AsyncMongoClient
from configuration.config import DB_URI, DB_CONTRIBUTOR

# For mongodb wiki articles database
client_1 = AsyncMongoClient(DB_URI, server_api=ServerApi("1"))
db = client_1.get_database("technoinc-db")

# For mongodb contributor database
client_2 = AsyncMongoClient(DB_CONTRIBUTOR, server_api=ServerApi("1"))
con_db = client_2.get_database("technoinc-db")