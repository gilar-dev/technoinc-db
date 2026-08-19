from configuration.database import db

# Delete article from database
def delete_article_wiki(data: dict):
    try:
        document = db["wiki-articles"]
        result = document.delete_one({ "id": data["article_id"] })

        return {
            "status": "Success",
            "message": str(result)
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }