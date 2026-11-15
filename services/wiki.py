import re, json
from typing import Any
from configuration import model
from configuration.database import db

async def get_article(title: str, field: str | None) -> dict[str, Any] | None:
    """Get article wiki or get its specific field (optional)"""
    try:
        collection = db.get_collection("wiki-articles")
        document: dict[str, Any] | None = await collection.find_one({
            "title": { "$regex": f"^{title}$", "$options": "i" }
        })
        if not document: return None
        
        document.pop("_id")
        get_redirect_arts = collection.find(
            { "content": { "$regex": f"\"type\":\"uni-redirect\",\"to\":\"{title}\"", "$options": "i" } },
            { "_id": 0, "title": 1 }
        )
        redirect_list = await get_redirect_arts.to_list()
        redirect_arts = [art.get("title") for art in redirect_list]

        return {
            "status": "Success",
            "data": document if not field else document.get(field),
            "redirect_arts": redirect_arts
        }
    
    except Exception as e:
        return { "status": "Error", "message": str(e) }

async def get_articles_sitemap() -> dict[str, Any]:
    """Get all existing articles to generate dynamic url sitemao"""
    try:
        collection = db.get_collection("wiki-articles")
        documents = collection.find({}, {
            "_id": 0, "title": 1, "cover": 1, "his": 1
        })
        articles: list[dict[str, str]] = await documents.to_list()
        title_list = [article.get("title") for article in articles]
        cover_list = [article.get("cover") for article in articles]
        modified_list = [json.loads(article["his"])[-1]["date"] for article in articles]
        return {
            "status": "Success",
            "title": title_list,
            "cover": cover_list,
            "date": modified_list
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }

async def get_matches_articles(input: str) -> dict[str, Any]:
    """Get existing matches articles from search input"""
    try:
        clean_input = input.strip()
        if not clean_input:
            return { "status": "Success", "articles": [] }
        
        collection = db.get_collection("wiki-articles")
        cursor = collection.find(
            { "title": { "$regex": f"^{re.escape(clean_input)}", "$options": "i" } },
            { "_id": 0, "title": 1, "desc": 1, "cover": 1 }
        )
        articles = await cursor.to_list(length=10)
        return { "status": "Success", "articles": articles }
    
    except Exception as e:
        return { "status": "Error", "message": str(e) }

async def check_links(data: model.LinkCheckRequest) -> dict[str, Any]:
    try:
        links = data.model_dump().get("links", [])
        regex_links = [re.compile(f"^{re.escape(link)}$", re.IGNORECASE) for link in links]
        collection = db.get_collection("wiki-articles")
        cursor = collection.find(
            { "title": { "$in": regex_links } },
            { "_id": 0, "title": 1 }
        )
        found_titles: list[dict[str, Any]] = await cursor.to_list(length=len(links))
        existing_links = [link.get("title") for link in found_titles]
        return { "status": "Success", "existing": existing_links }
    except Exception as e:
        return { "status": "Error", "message": str(e) }