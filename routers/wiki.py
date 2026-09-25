import re, json
from fastapi import APIRouter, HTTPException, status
from database import create, read, update, delete
from configuration import model
from configuration.database import db

router = APIRouter(prefix="/api/v1/wiki", tags=["Wiki"])

# Get article by matches input value
@router.get("/search/{title}")
async def search_article(title: str):
    try:
        clean_title = title.strip()
        if not clean_title:
            return { "status": "Success", "articles": [] }

        collection = db.get_collection("wiki-articles")
        cursor = collection.find(
            { "title": { "$regex": re.escape(clean_title), "$options": "i" } },
            { "_id": 0, "title": 1, "cover": 1, "desc": 1 }
        )
        articles = await cursor.to_list(length=20)

        return {
            "status": "Success",
            "articles": articles
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Delete article from database
@router.delete("/delete")
async def delete_article_wiki(data: model.ArticleInit):
    return delete.delete_article_wiki(data.model_dump())

# Create new category
@router.post("/category/create")
async def create_category(data: model.WikiCreateCategory):
    return create.create_category(data.model_dump())

# === IMPORTANT AND FIXED ===
# Get article wiki by category and id
@router.get("/get/{article_id}")
async def get_article_wiki(article_id: str, field: str = ""):
    return await read.get_article_wiki(article_id, field)

# Get category from input
@router.get("/category/search/{input}")
async def get_category(input: str):
    return await read.get_category(input)

# Get article id to add visited value
@router.put("/view")
async def initialize_ttl(data: model.ArticleInit):
    return update.increase_visited(data.model_dump())

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
        collection.update_one(
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

# Check link validations from article title
@router.post("/check-links")
async def check_links(data: model.LinkCheckRequest):
    """Check link validations from article title"""
    try:
        links = data.model_dump().get("links", [])
        collection = db["wiki-articles"]
        cursor = collection.find(
            { "title": { "$in": links } },
            { "title": 1, "_id": 0 }
        )
        found_titles = await cursor.to_list(length=len(links))
        existing_titles = [doc["title"] for doc in found_titles]
        return {
            "status": "Success",
            "existing": existing_titles
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/articles")
async def get_articles():
    try:
        collection = db["wiki-articles"]
        documents = collection.find(
            {}, { "_id": 0, "title": 1, "cover": 1, "his": 1 }
        )
        articles = await documents.to_list()
        title_list = [article["title"] for article in articles]
        cover_list = [article["cover"] for article in articles]
        modified_list = [json.loads(article["his"])[-1]["date"] for article in articles]
        return {
            "status": "Success",
            "title": title_list,
            "cover": cover_list,
            "date": modified_list
        }
    except Exception as e:
        print(e)
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