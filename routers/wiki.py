from fastapi import APIRouter
from configuration import model
from database import read, create

router = APIRouter(prefix="/api/v1/wiki", tags=["Wiki"])

# Get article categories
@router.get("/categories")
async def get_article_categories():
    return read.get_article_categories()

# Upload or create new article
@router.post("/upload")
async def upload_wiki_article(payload: model.WikiArticlePayload):
    return create.upload_wiki_article(payload.model_dump())

# Get articles list by category
@router.get("/{category}/articles")
async def get_articles_by_category(category: str):
    return read.get_articles_by_category(category)

# Get article existence
@router.get("/{category}/{article_id}/exist")
async def check_article_id(category: str, article_id: str):
    return read.check_article_id(category, article_id)

# Get article wiki by category and id
@router.get("/{category}/{article_id}")
async def get_article_wiki(category: str, article_id:str):
    return read.get_article_wiki(category, article_id)