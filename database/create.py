from configuration.database import db

# Create new category
def create_category(data: dict):
    try:
        collection = db["wiki-categories"]
        collection.insert_one({
            "category": data["category_name"],
            "parent": data["category_parent"]
        })

        return {
            "status": "Success",
            "message": "New category is successfully created"
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }