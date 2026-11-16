import json
from configuration.model import WikiArticlePayload
from configuration.database import db
from services import telegram

async def upload_article_wiki(payload: WikiArticlePayload):
    """Upload new article payload to database"""
    try:
        document = db.get_collection("wiki-articles")
        # Insert new article on available collection
        await document.insert_one(payload.model_dump())
        await telegram.send_created_article(payload.title, json.loads(payload.his[-1]))
        return {
            "status": "Success",
            "url": f"/wiki/{payload.title}"
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }

async def update_article_wiki(payload: WikiArticlePayload):
    """Update edited article payload to database"""
    try:
        loaded_data = payload.model_dump()
        loaded_data.pop("ver", None)
        modify_info = json.loads(payload.his)[-1]
        document = db.get_collection("wiki-articles")
        # Update document
        await document.update_one(
            { "id": payload.id }, 
            { "$set": loaded_data, "$inc": { "ver": 1 } }
        )
        # Send notification to telegram Farel
        await telegram.send_updated_article(payload.title, modify_info)
        return {
            "status": "Success",
            "message": f"Article with title '{payload.title}' is successfully updated"
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }