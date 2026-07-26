from fastapi import APIRouter
from database import read, update, delete
from configuration.model import ArticleInit

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
async def initialize_ttl(data: ArticleInit):
    return update.increase_visited(data.model_dump())

# Delete article from database
@router.delete("/delete")
async def delete_article_wiki(data: ArticleInit):
    return delete.delete_article_wiki(data.model_dump())

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