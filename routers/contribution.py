from fastapi import APIRouter
from configuration import model
from configuration.database import db
from database import create, update

router = APIRouter(prefix="/api/v1/contribution", tags=["Contribution"])

# Upload or create new article
@router.post("/upload")
async def upload_wiki_article(payload: model.WikiArticlePayload):
    """Upload new article payload to database"""
    try:
        article_data = payload.model_dump()
        document = db["wiki-articles"]
        # Insert new article on available collection
        await document.insert_one(article_data)
        return {
            "status": "Success",
            "url": f"/wiki/{article_data["title"]}"
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }

# Update article from contribution models
@router.patch("/update")
async def update_article(article_data: model.WikiArticlePayload):
    """Update edited article payload to database"""
    try:
        loaded_data = article_data.model_dump()
        loaded_data.pop("ver", None)
        document = db["wiki-articles"]
        # Update document
        await document.update_one(
            { "id": loaded_data["id"] }, 
            { "$set": loaded_data, "$inc": { "ver": 1 } }
        )
        return {
            "status": "Success",
            "message": f"Article with title '{article_data["title"]}' is successfully updated"
        }
    except Exception as e:
        print(e)
        return { "status": "Error", "message": str(e) }