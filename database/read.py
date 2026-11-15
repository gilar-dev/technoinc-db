from configuration.database import db

# Get category from input
async def get_category(category: str):
    matches: list[dict[str, str]] = []

    async def fetch_main_categories():
        cursor = db["wiki-main-categories"].find({})
        main_categories = await cursor.distinct("categories")
        for cat in main_categories:
            category_name: str = cat
            if category.lower() in category_name.lower():
                matches.append({ "category": cat, "hierarchy": "Main category" })

    async def fetch_categories():
        cursor = db["wiki-categories"].find(
            { "category": { "$regex": category, "$options": "i" } },
            { "_id": 0, "category": 1, "parent": 1 }
        )
        categories = await cursor.to_list(length=10)
        for cat in categories:
            matches.append({ "category": cat["category"], "hierarchy": f"Subcategory of {cat["parent"]}" })
            
    try:
        await fetch_main_categories()
        await fetch_categories()

        return {
            "status": "Success",
            "data": matches
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }