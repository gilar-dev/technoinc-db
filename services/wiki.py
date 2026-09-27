import json
from fastapi import Query
from typing import Optional
from configuration import model
from configuration.database import db

async def get_article(title: str, field: str = Query(...)):
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

async def get_articles_sitemap():
    """Get all existing articles to generate dynamic url sitemao"""
    try:
        collection = db.get_collection("wiki-articles")
        documents = collection.find({}, {
            "_id": 0, "title": 1, "cover": 1, "his": 1
        })
        articles: list[dict] = await documents.to_list()
        title_list = [article.get("title") for article in articles]
        cover_list = [article.get("cover") for article in articles]
        modified_list = [json.loads(article.get("his"))[-1]["date"] for article in articles]
        return {
            "status": "Success",
            "title": title_list,
            "cover": cover_list,
            "date": modified_list
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }