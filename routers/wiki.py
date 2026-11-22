import re, json
from fastapi import APIRouter, HTTPException, status
from typing import Optional, Literal, Any
from database import create, read
from services import wiki
from configuration import model
from model.article_model import *
from model.error_model import ErrorModel
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
async def get_article_info(title: str) -> ArticleInformationModel | ErrorModel | None:
    try:
        collection = db.get_collection("wiki-articles")
        document = await collection.find_one(
            { "title": { "$regex": f"^{title}$", "$options": "i" }}
        )
        if not document: return

        document.pop("_id") # Remove unnecessary property
        content: str = document["content"]
        content_length = len(content.encode("utf-8"))

        # For article page information
        history: list[dict[str, Any]] = json.loads(document["his"])
        creator = history[0].get("user")
        creation_date = history[0].get("date")
        latest_editor = history[-1].get("user")
        latest_edit_date = history[-1].get("date")

        # For article property
        categories: list[str] = json.loads(document["cat"])

        return ArticleInformationModel(
            status="Success",
            data=ArticleInformationData(
                basic_info=Basicinfo(
                    title=str(document["title"]),
                    content_length=content_length,
                    id=int(document["id"]),
                    view=int(document["view"]),
                    description=str(document["desc"]),
                    cover=str(document["cover"])
                ),
                edit_history=EditHistory(
                    creator=str(creator),
                    creation_date=str(creation_date),
                    latest_editor=str(latest_editor),
                    latest_edit_date=str(latest_edit_date),
                    total_edit=int(document["ver"])
                ),
                property=Property(
                    categories=categories
                )
            )
        )

    except Exception as e:
        return ErrorModel(
            status="Error",
            message=str(e)
        )