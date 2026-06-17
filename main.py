from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Initialize server
app = FastAPI()

DB_URL = "mongodb+srv://TechnoIncDatabase:TechnoBase53261@technoinccluster.tvawecx.mongodb.net/?appName=TechnoIncCluster"
client = MongoClient(DB_URL, server_api=ServerApi("1"))

# Define the allowed fetch origins
origins = [
    "https://technoinc.world",
    "https://technoinc.netlify.app",
    "http://localhost:5173"
]

# Add middleware configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Initialize database
db = client["technoinc_db"]

# Initialize database collections
civilizations = db["civilizations"]
organizations = db["organizations"]


@app.get("/")
def entry():
    try:
        client.admin.command("ping")

        return {
            "status": "Success",
            "message": "Welcome to the official API of TechnoInc World!",
            "category_list": [
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


@app.get("/api/v1/collections")
def get_collections():
    try:
        collections_list = db.list_collection_names()

        return {
            "status": "Success",
            "collections": collections_list
        }
    
    except Exception as e:
        pass


@app.get("/api/v1/admin-contribution")
def get_contribution_key():
    try:
        key = db["admin-contribution"].distinct("key")

        return {
            "key": int(key[0])
        }
    
    except Exception as e:
        return {
            "status": "Failed",
            "message": str(e)
        }
    

@app.get("/api/v1/organizations")
def get_organizations():
    try:
        raw_data = civilizations.find()
        clean_list = []

        for document in raw_data:
            document["_id"] = str(document["_id"])
            clean_list.append(document)

        return {
            "status": "Success",
            "totalRecords": len(clean_list),
            "data": clean_list 
        }
    
    except Exception as e:
        return {
            "error": str(e)
        }