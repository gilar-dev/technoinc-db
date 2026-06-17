from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Import from locals
from config import configuration as config

# Initialize server
app = FastAPI()
client = MongoClient(config.DB_URL, server_api=ServerApi("1"))

# Add middleware configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins = config.origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Initialize database
db = client["technoinc_db"]

# Entry url
@app.get("/")
def entry():
    try:
        return {
            "status": "Success",
            "message": "Welcome to the official API of TechnoInc World!",
            "categoryList": [
                "Civilizations",
                "Characters",
                "Ideologies",
                "Organizations",
                "Parties",
                "Towns"
            ]
        }
    
    except Exception as e:
        return {
            "status": "Error",
            "message": str(e)
        }
    
@app.get("/api/v1/categories")
def get_categories():
    try:
        category_list = db["categories"].distinct("categoryList")

        return {
            "status": "Success",
            "categoryList": category_list
        }
    
    except Exception as e:
        return { "status": "Error", "message": str(e) }

@app.get("/api/v1/collections")
def get_collections():
    try:
        collections_list = db.list_collection_names()

        return {
            "status": "Success",
            "collections": collections_list
        }
    
    except Exception as e:
        return { "status": "Failed", "message": str(e) }

@app.get("/api/v1/admin-contribution")
def get_contribution_key():
    try:
        key = db["admin-contribution"].distinct("key")

        return {
            "key": int(key[0])
        }
    
    except Exception as e:
        return { "status": "Failed", "message": str(e) }    