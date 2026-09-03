from configuration.database import db
    
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
    
# Get all articles of all categories
def get_all_articles():
    try:
        collections = db.list_collection_names()
        # Filter only cllection with category
        categories = [cat for cat in collections if cat.startswith("cat-")]
        # Empty list for articles data
        articles = []

        for cat in categories:
            # Get all articles from category name
            document = db[cat].find({})

            if document:
                # Loop through document
                for doc in document:
                    # Delete unnecessary property
                    if "_id" in doc:
                        del doc["_id"]
                        del doc["wiki_content"]

                    articles.append(doc)

        return {
            "status": "Success",
            "data": articles
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }

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
def get_category(category: str):
    try:
        main_categories = db["wiki-main-categories"]
        sub_categories = db["wiki-categories"]
        matches: list[dict] = [] # List of matches category by input

        # Find matches category with main categories
        with main_categories.find() as cursor:
            for document in cursor:
                for categories in document["categories"]:
                    cat: str = categories
                    if category.lower() in cat.lower():
                        matches.append({ "category": cat, "hierarchy": "Main category" })

        # Find matches category with existed sub categories
        with sub_categories.find() as cursor:
            for document in cursor:
                # Skip if key of 'category_list' is in document
                if "category_list" in document:
                    continue
                sub_category: str = document["category"]
                if category.lower() in sub_category.lower():
                    matches.append({ "category": sub_category, "hierarchy": f"Subcategory of {document["parent"]}" })

        if len(matches) >= 10:
            matches = matches[:10]

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
async def get_article_wiki(article_id: str, option: str = ""):
    try:
        collection = db["wiki-articles"]
        formatted_id = article_id.replace("_", " ")
        document = await collection.find_one({
            "title": { "$regex": f"^{formatted_id}$", "$options": "i" }
        })

        if not document:
            return {
                "status": "Error",
                "message": f"Article with id '{article_id}' not found."
            }

        document.pop("_id", None)
        return {
            "status": "Success",
            "article": document if option == "" else document[option]
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

# Get current universal id value
def get_universal_id():
    try:
        # Initializing document
        document = db["wiki-configurations"]
        # Getting universal id value from document
        universal_id: int = document.distinct("universal_id", { "type": "configurations" })[0]

        # Return successful getting universal value
        return {
            "status": "Success",
            "universal_id": universal_id
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }