from configuration.database import db

# Get article by input value
def search_article(input: str):
    try:
        collections: list[str] = db.list_collection_names()
        categories: list[str] = [x for x in collections if x.startswith("cat-")]

        # Empty list to contain matches article from input
        matches: list[str] = []
        for cat in categories:
            # Check articles in all categories
            document = db[cat]
            with document.find() as cursor:
                for doc in cursor:
                    # Get article title
                    title: str = doc["title"]
                    if input.lower() in title.lower():
                        # Delete unnecessary property
                        del doc["_id"]
                        del doc["wiki_content"]
                        matches.append(doc)

        return {
            "status": "Success",
            "matches": matches
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }

# Check article existence
def check_article_id(category: str, article_id: str):
    try:
        collection = f"cat-{category.lower()}"
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

# Get category from input
async def get_category(category: str):
    matches: list[str] = []

    async def fetch_main_categories():
        cursor = db["wiki-main-categories"].find({})
        main_categories = await cursor.distinct("categories")
        for cat in main_categories:
            category_name: str = cat
            if category.lower() in category_name.lower():
                matches.append({ "category": cat, "hierarchy": "Main category" })

    async def fetch_categories():
        cursor = db["wiki-categories"].find(
            { "category": { "$regex": category, "$options": "i" } },
            { "_id": 0, "category": 1, "parent": 1 }
        )
        categories = await cursor.to_list(length=10)
        for cat in categories:
            matches.append({ "category": cat["category"], "hierarchy": f"Subcategory of {cat["parent"]}" })
            
    try:
        await fetch_main_categories()
        await fetch_categories()

        return {
            "status": "Success",
            "data": matches
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }
    
# Get article list by category
def get_articles_by_category(category: str):
    try:
        converted_category = f"cat-{category}"
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

# === IMPORTANT AND FIXED ===
# Get article wiki by category and id
async def get_article_wiki(article_id: str, field: str = ""):
    try:
        collection = db.get_collection("wiki-articles")
        document: dict = await collection.find_one({
            "title": { "$regex": f"^{article_id}$", "$options": "i" }
        })
        if not document:
            return
        document.pop("_id", None)
        return {
            "status": "Success",
            "article": document if field == "" else document[field]
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }

# Check article existence
def check_article_title(article_title: str):
    try:
        document = db["wiki-articles"]
        is_exist: bool = False

        with document.find() as cursor:
            for article in cursor:
                title: str = article["title"]

                if title.lower().replace(" ", "") == article_title:
                    is_exist = True

        return {
            "status": "Success",
            "is_exist": is_exist
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }