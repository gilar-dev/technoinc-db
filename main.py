from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

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
    wikiContent: List[Dict[str, Any]]

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
            "message": f"For some reason, it's not allowed!, {e}"
        }  