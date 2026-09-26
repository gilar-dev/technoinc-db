from typing import Optional
from configuration import model
from configuration.database import db

async def get_article(title: str, field: Optional[str]):
    """Get article wiki or get its specific field (optional)"""
    try:
        collection = db.get_collection("wiki-articles")
        document: dict = await collection.find_one({
            "title": { "$regex": f"^{title}$", "$options": "i" }
        })
        if not document: return None
        document.pop("_id")
        return {
            "status": "Success",
            "data": document if not field else document.get(field)
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }