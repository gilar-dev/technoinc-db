import json
from configuration import model
from configuration.database import db
from services import telegram

async def upload_article_wiki(payload: model.WikiArticlePayload):
    """Upload new article payload to database"""
    try:
        article_data = payload.model_dump()
        document = db.get_collection("wiki-articles")
        # Insert new article on available collection
        await document.insert_one(article_data)
        await telegram.send_created_article(article_data.get("title"), json.loads(article_data.get("his")[-1]))
        return {
            "status": "Success",
            "url": f"/wiki/{article_data["title"]}"
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }

async def update_article_wiki(article_data: model.WikiArticlePayload):
    """Update edited article payload to database"""
    try:
        loaded_data = article_data.model_dump()
        loaded_data.pop("ver", None)
        modify_info = json.loads(loaded_data.get("his"))[-1]
        document = db.get_collection("wiki-articles")
        # Update document
        await document.update_one(
            { "id": loaded_data["id"] }, 
            { "$set": loaded_data, "$inc": { "ver": 1 } }
        )
        # Send notification to telegram TechnoBot
        await telegram.send_updated_article(loaded_data.get("title"), modify_info)
        return {
            "status": "Success",
            "message": f"Article with title '{article_data["title"]}' is successfully updated"
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }