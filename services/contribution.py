import json
from pydantic import BaseModel
from typing import Literal
from configuration.database import db
from model.article_model import ArticleModel
from services import telegram

class ReturnData(BaseModel):
    status: Literal["Success", "Error"]
    message: str

async def upload_article_wiki(payload: ArticleModel) -> ReturnData:
    """Upload new article payload to database"""
    try:
        loaded_data = payload.model_dump()
        stringified_his = { "his": json.dumps(loaded_data.get("his")) }
        stringified_content = { "content": json.dumps(loaded_data.get("content")) }

        # Insert new article on available collection
        document = db.get_collection("wiki-articles")
        await document.insert_one({ **loaded_data, **stringified_his, **stringified_content })

        # Send notification to telegram FarelBot
        modify_info = payload.his[-1]
        await telegram.send_created_article(payload.title, telegram.ModifyInfo(
            user=modify_info.user,
            sum=modify_info.sum,
            date=modify_info.date
        ))

        return ReturnData(
            status="Success",
            message=f"Article '{payload.title.replace("_", " ")}' is successfully created"
        )
    
    except Exception as e:
        return ReturnData(status="Error", message=str(e))

async def update_article_wiki(payload: ArticleModel) -> ReturnData:
    """Update edited article payload to database"""
    try:
        loaded_data = payload.model_dump()
        loaded_data.pop("ver", None) # Delete current version for atomic operation
        stringified_his = { "his": json.dumps(loaded_data.get("his")) }
        stringified_content = { "content": json.dumps(loaded_data.get("content")) }

        # Update document
        document = db.get_collection("wiki-articles")
        await document.update_one(
            { "id": payload.id }, 
            { "$set": { **loaded_data, **stringified_his, **stringified_content }, "$inc": { "ver": 1 } }
        )

        # Send notification to telegram FarelBot
        modify_info = payload.his[-1]
        await telegram.send_updated_article(payload.title, telegram.ModifyInfo(
            user=modify_info.user,
            sum=modify_info.sum,
            date=modify_info.date
        ))

        return ReturnData(
            status="Success",
            message=f"Article '{payload.title.replace("_", " ")}' is successfully updated"
        )
    
    except Exception as e:
        print(e)
        return ReturnData(status="Error", message=str(e))