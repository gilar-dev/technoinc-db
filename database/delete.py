from configuration.database import db

# Delete article from database
def delete_article_wiki(category: str, article_id: str):
    try:
        collection = f"cat-{category}"
        document = db[collection]
        result = document.delete_one({ "id": article_id })

        return {
            "status": "Success",
            "message": str(result)
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }