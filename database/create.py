from configuration.database import db

# Upload or create new article
def upload_wiki_article(article_data: dict):
    try:
        article_id = article_data["id"]
        article_category = article_data["category"]

        # Convert category name to find the collection
        collection = "cat-" + article_category.lower()

        # Check if collection it's not exist
        collections_list = db.list_collection_names()
        if not collection in collections_list:
            db.create_collection(collection)

        db[collection].insert_one(article_data)

        return {
            "status": "Success",
            "message": f"Article '{article_data["title"]}' is successfully sent to database!",
            "id": article_id
        }
    
    except Exception as e:
        return { "status": "Error", "message": str(e) }