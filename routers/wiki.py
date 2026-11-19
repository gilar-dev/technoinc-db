import re
from fastapi import APIRouter, HTTPException, status
from typing import Optional, Literal
from database import create, read
from services import wiki
from configuration import model
from configuration.database import db

router = APIRouter(prefix="/api/v1/wiki", tags=["Wiki"])

# Create new category
@router.post("/category/create")
async def create_category(data: model.WikiCreateCategory):
    return create.create_category(data.model_dump())

# === IMPORTANT AND FIXED ===
@router.get("")
async def entry(field: Literal["random", "total"]):
    if field == "random":
        return await wiki.wiki_random()
    elif field == "total":
        return await wiki.wiki_total()

@router.post("/check-links")
async def check_links(data: model.LinkCheckRequest):
    return await wiki.check_links(data)

@router.get("/articles/sitemap")
async def get_articles_sitemap():
    return await wiki.get_articles_sitemap()

@router.get("/search/{input}")
async def get_matches_articles(input: str):
    return await wiki.get_matches_articles(input)

# Get category from input
@router.get("/category/search/{input}")
async def get_category(input: str):
    return await read.get_category(input)

# Get universal id value from database
@router.get("/universal-id/get")
async def get_universal_id():
    """Get universal id value from database"""
    try:
        collection = db["wiki-configurations"]
        document = await collection.find_one(
            { "type": "configurations" },
            { "un_id": 1, "_id": 0 }
        )
        if not document: return None

        return { "status": "Success", "universal_id": document["un_id"] }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Update universal id by increasing its value
@router.put("/universal-id/increase")
async def increase_universal_id():
    """Update universal id value by increasing it"""
    try:
        collection = db["wiki-configurations"]
        await collection.update_one(
            { "type": "configurations" },
            { "$inc": { "un_id": 1 } }
        )
        return {
            "status": "Success",
            "message": "Universal Id is successfully increased"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Check article title existence in database
@router.get("/articles/{title}/check-exist")
async def check_title_existence(title: str):
    """Check article title existence in database"""
    try:
        pattern = f"^{re.escape(title)}$"
        collection = db["wiki-articles"]
        document = await collection.find_one(
            { "title": { "$regex": pattern, "$options": "i" }},
            { "_id": 1 }
        )
        is_exist = True if document else False
        return { "status": "Success", "is_exist": is_exist }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{title}")
async def get_article(title: str, field: Optional[str] = ""):
    return await wiki.get_article(title, field)

@router.get("/{title}/info")
async def get_article_info(title: str):
    try:
        collection = db.get_collection("wiki-articles")
        document = await collection.find_one(
            { "title": { "$regex": f"^{title}$", "$options": "i" }}
        )
        if not document: return

        document.pop("_id")
        content: str = document["content"]
        content_length = len(content.encode("utf-8"))

        return {
            "status": "Success",
            "data": {
                "title": document.get("title"),
                "content_length": content_length,
                "id": document.get("id"),
                "view": document.get("view"),
                "description": document.get("desc"),
                "cover": document.get("cover")
            }
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }