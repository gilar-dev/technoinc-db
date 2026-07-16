from configuration.database import db

# Delete article from database
def delete_article_wiki(data: dict):
    try:
        collection = f"cat-{data.category}"
        document = db[collection]
        result = document.delete_one({ "id": data.article_id })

        return {
            "status": "Success",
            "message": str(result)
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }