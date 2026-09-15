from configuration.database import db
    
# Increase article visited value
def increase_visited(data: dict):
    try:
        # Define article collection
        collection = db["wiki-articles"]
        print(data.get("article_id"))

        # Increase article visit
        collection.update_one(
            { "id": data.get("article_id") },
            { "$inc": { "visited": 1 } }
        )

        return {
            "status": "Success",
            "message": f"Article '{data["id"]}' visited is successfully increased"
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }