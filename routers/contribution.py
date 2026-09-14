from fastapi import APIRouter
from configuration import model
from configuration.database import db
from database import create, update

router = APIRouter(prefix="/api/v1/contribution", tags=["Contribution"])

# Upload or create new article
@router.post("/upload")
async def upload_wiki_article(payload: model.WikiArticlePayload):
    try:
        article_data = payload.model_dump()
        collection = db["wiki-articles"]
        # Insert new article on available collection
        collection.insert_one(article_data)
        return {
            "status": "Success",
            "url": f"/wiki/{article_data["title"]}"
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }

# Update article from contribution models
@router.patch("/update")
async def update_article(article_data: model.WikiArticlePayload):
    return update.update_article(article_data.model_dump())