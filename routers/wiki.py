from fastapi import APIRouter
from database import create, read, update, delete
from configuration import model

router = APIRouter(prefix="/api/v1/wiki", tags=["Wiki"])

# Get article categories
@router.get("/categories")
async def get_article_categories():
    return read.get_article_categories()

# Get all articles of all categories
@router.get("/articles")
async def get_all_articles():
    return read.get_all_articles()

# Get article by matches input value
@router.get("/search/{input}")
async def search_article(input: str):
    return read.search_article(input)

# Get article id to add visited value
@router.put("/view")
async def initialize_ttl(data: model.ArticleInit):
    return update.increase_visited(data.model_dump())

# Delete article from database
@router.delete("/delete")
async def delete_article_wiki(data: model.ArticleInit):
    return delete.delete_article_wiki(data.model_dump())

# Create new category
@router.post("/category/create")
async def create_category(data: model.WikiCreateCategory):
    return create.create_category(data.model_dump())

# Get category from input
@router.get("/category/search/{input}")
async def get_category(input: str):
    return read.get_category(input)

# Get articles list by category
@router.get("/{category}/articles")
async def get_articles_by_category(category: str):
    return read.get_articles_by_category(category)

# Get article existence
@router.get("/{category}/{article_id}/exist")
async def check_article_id(category: str, article_id: str):
    return read.check_article_id(category, article_id)

# === IMPORTANT AND FIXED ===
# Get article wiki by category and id
@router.get("/get/{article_id}")
async def get_article_wiki(article_id:str, option: str = ""):
    return read.get_article_wiki(article_id, option)

# Check article existence
@router.get("/check/{article_title}")
async def check_article_title(article_title: str):
    return read.check_article_title(article_title)

# Get universal id value
@router.get("/universal_id/get")
async def get_universal_id():
    return read.get_universal_id()

# Update universal id by increasing its value
@router.put("/universal_id/increase")
async def increase_universal_id():
    return update.increase_universal_id()