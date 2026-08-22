from configuration.database import db

# Update article from contribution mode
def update_article(article_data: dict):
    try:
        # Initializing document
        document = db["wiki-articles"]

        if "version" in article_data:
            del article_data["version"]

        # Update document
        document.update_one(
            { "id": article_data["id"] }, 
            { "$set": article_data, "$inc": { "version": 1 } }
        )

        return {
            "status": "Success",
            "message": f"Article with title '{article_data["title"]}' is successfully updated"
        }

    except Exception as e:
        print(e)
        return { "status": "Error", "message": str(e) }
    
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

# Increase universal wiki id
def increase_universal_id():
    try:
        # Initializing document
        document = db["wiki-configurations"]
        # Updating universal id
        document.update_one(
            { "type": "configurations" },
            { "$inc": { "universal_id": 1 } }
        )

        # Return successful updating status
        return {
            "status": "Success",
            "message": "Universal Id is successfully increased"
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }