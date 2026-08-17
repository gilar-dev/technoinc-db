from fastapi import APIRouter
from configuration import model
from database import create, update

router = APIRouter(prefix="/api/v1/contribution", tags=["Contribution"])

# Upload or create new article
@router.post("/upload")
async def upload_wiki_article(payload: model.WikiArticlePayload):
    return create.upload_wiki_article(payload.model_dump())

# Update article from contribution models
@router.put("/update")
async def update_article(article_data: model.WikiArticlePayload):
    return update.update_article(article_data.model_dump())