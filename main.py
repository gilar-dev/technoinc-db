# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Locals
from configuration import config, model
from database import create, read

# Initialize server
app = FastAPI()

# Add middleware configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins = config.origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Entry url
@app.get("/")
async def entry():
    return read.entry()

# Get article categories
@app.get("/api/v1/wiki/categories")
async def get_article_categories():
    return read.get_article_categories()

# Get articles list by category
@app.get("/api/v1/wiki/{category}/articles")
async def get_articles_by_category(category: str):
    return read.get_articles_by_category(category)

# Get article existence
@app.get("/api/v1/wiki/{category}/{article_id}/exist")
async def check_article_id(category: str, article_id: str):
    return read.check_article_id(category, article_id)

# Get article wiki by category and id
@app.get("/api/v1/wiki/{category}/{article_id}")
async def get_article_wiki(category: str, article_id:str):
    return read.get_article_wiki(category, article_id)

# Upload or create new article
@app.post("/api/v1/wiki/upload")
async def upload_wiki_article(payload: model.WikiArticlePayload):
    return create.upload_wiki_article(payload.model_dump())