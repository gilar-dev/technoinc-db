from configuration.database import db

# Entry URL
def entry():
    try:
        return {
            "status": "Success",
            "message": "Welcome to the official API of TechnoInc World!",
            "website": "https://technoinc.world",
            "description": "Start reading a journey of five years Minecraft survival world!"
        }
    
    except Exception as e:
        return { "status": "Error", "message": str(e) }
    
# Get article categories
def get_article_categories():
    try:
        # Get categories
        categories = db["wiki-categories"].distinct("category_list")

        return {
            "status": "Success",
            "category_list": categories
        }
    
    except Exception as e:
        return { "status": "Error", "message": str(e) }

# check article existence
def check_article_id(category: str, article_id: str):
    try:
        collection = "cat-" + category.lower()
        document = db[collection].find_one({ "id": article_id })

        # Check if document with given id is exist or not
        is_exist = True if document else False
        
        # Delete unnecessary property
        if "_id" in document:
            del document["_id"]

        return {
            "status": "Success",
            "is_exist": is_exist
        }
    
    except Exception as e:
        return { "status": "Error", "message": str(e) }
    
# Get article list by category
def get_articles_by_category(category: str):
    try:
        converted_category = "cat-" + category
        collection = db[converted_category]

        # Get all articles from a category
        articles = collection.find({})

        article_list = []
        for article in articles:
            # Delete unnecessary property
            if "_id" in article:
                del article["_id"]

            article_list.append(article)

        return {
            "status": "Success",
            "articles": article_list
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }
    
# Get article wiki by category and id
def get_article_wiki(category: str, article_id: str):
    try:
        converted_category = "cat-" + category
        document = db[converted_category]

        # Find document based on article id
        results = document.find_one({ "id": article_id })

        # Delete unnecessary property
        if "_id" in results:
            del results["_id"]

        return {
            "status": "Success",
            "article": results
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }