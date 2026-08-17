from configuration.database import db

# Upload or create new article
def upload_wiki_article(article_data: dict):
    try:
        # Set where article document stored on specific collection
        collection = db["wiki-articles"]
        # Insert new article on available collection
        collection.insert_one(article_data)

        return {
            "status": "Success",
            "message": f"Article '{article_data["title"]}' is successfully sent to database!",
            "id": article_data["id"]
        }
    
    except Exception as e:
        return { "status": "Error", "message": str(e) }

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