from configuration.database import db

# Update article from contribution mode
def update_article(category: str, article_data: dict):
    try:
        collection = f"cat-{category.lower()}"
        document = db[collection]

        # Update document
        document.update_one(
            { "id": article_data["id"] }, 
            { "$set": { "wiki_content": article_data["wiki_content"] } }
        )

        return {
            "status": "Success",
            "message": f"Article with id '{article_data["id"]}' is successfully updated"
        }

    except Exception as e:
        print(e)
        return { "status": "Error", "message": str(e) }