from fastapi import APIRouter
from model.article_model import ArticleModel
from services import contribution

router = APIRouter(prefix="/api/v1/contribution", tags=["Contribution"])

# Upload or create new article
@router.post("/upload")
async def upload_article_wiki(payload: ArticleModel):
    return await contribution.upload_article_wiki(payload)

# Update article from contribution models
@router.patch("/update")
async def update_article_wiki(article_data: ArticleModel):
    return await contribution.update_article_wiki(article_data)