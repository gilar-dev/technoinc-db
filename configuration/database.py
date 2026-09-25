from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
from configuration.config import DB_WIKI, DB_CONTRIBUTOR

# For mongodb wiki articles database
client_1 = AsyncIOMotorClient(DB_WIKI, server_api=ServerApi("1"))
db = client_1.get_database("technoinc-db")

# For mongodb contributor database
client_2 = AsyncIOMotorClient(DB_CONTRIBUTOR, Server_api=ServerApi("1"))
con_db = client_2.get_database("technoinc-db")