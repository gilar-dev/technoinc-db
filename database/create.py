from typing import Any
from configuration.database import db

# Create new category
async def create_category(data: dict[str, Any]):
    try:
        collection = db["wiki-categories"]
        await collection.insert_one({
            "category": data["category_name"],
            "parent": data["category_parent"]
        })

        return {
            "status": "Success",
            "message": "New category is successfully created"
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }