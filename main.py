from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from typing import List, Dict, Any

# Import from locals
from configuration import config

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

class WikiArticlePayload(BaseModel):
    id: str
    title: str
    category: str
    visited: int = 0
    wiki_content: List[Dict[str, Any]]

# Initialize database
db = client["technoinc_db"]

# Entry url
@app.get("/")
def entry():
    try:
        return {
            "status": "Success",
            "message": "Welcome to the official API of TechnoInc World!",
            "website": "https://technoinc.world",
            "description": "Start reading a journey of five years Minecraft survival world!"
        }
    
    except Exception as e:
        return {
            "status": "Error",
            "message": str(e)
        }
    
@app.get("/api/v1/categories")
def get_categories():
    try:
        category_list = db["categories"].distinct("category_list")

        return {
            "status": "Success",
            "category_list": category_list
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

@app.post("/api/v1/wiki/upload")
async def upload_wiki_article(payload: WikiArticlePayload):
    try:
        article_data = payload.model_dump()
        article_id = article_data["id"]

        db["wiki_articles"].update_one(
            { "id": article_id },
            { "$set": article_data },
            upsert=True
        )

        return {
            "status": "Success",
            "message": f"Article '{article_data["title"]}' successfully sent to database!",
            "id": article_id,
            "data": str(article_data)
        }

    except Exception as e:
        return {
            "status": "Error",
            "message": str(e)
        }
    
@app.get("/api/v1/wiki/{article_id}")
async def check_article_id(article_id: str):
    try:
        document = db["wiki_articles"].find_one({ "id": article_id })

        # Check if document with given id is exist or not
        is_exist = True if document else False
        
        if "_id" in document:
            del document["_id"]

        return {
            "status": "Success",
            "is_exist": is_exist
        }
    
    except HTTPException as http_error:
        return { "status": "Error", "message": str(http_error) }
    except Exception as e:
        return { "status": "Error", "mesage": str(e) }