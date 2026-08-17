from configuration.database import db

# Update article from contribution mode
def update_article(article_data: dict):
    try:
        # Initializing document
        document = db["wiki-articles"]

        # Update document
        document.update_one(
            { "id": article_data["id"] }, 
            { "$set": article_data }
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

        # Find matches article with id
        with collection.find() as cursor:
            for document in cursor:
                print(document)
                document_id: str = document["id"]
                if document_id.lower() == data["id"]:
                    document.update_one({
                        "$inc": { "visited": 1 }
                    })

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