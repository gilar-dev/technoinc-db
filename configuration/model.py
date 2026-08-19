from pydantic import BaseModel
from typing import List, Dict, Any

# Model for initializing upload article
class WikiArticlePayload(BaseModel):
    title: str
    id: int
    description: str
    cover: str
    public_id: str
    visited: int
    classification: str
    category: List[str]
    history: List[Dict[str, Any]]
    wiki_content: List[Dict[str, Any]]

# Model for initializing update article
class WikiArticleUpdate(BaseModel):
    id: str
    wiki_content: List[Dict[str, Any]]

# Model for creating new wiki category
class WikiCreateCategory(BaseModel):
    category_name: str
    category_parent: str

# Model for getting assets public id
class ImagePublicId(BaseModel):
    folder_name: str
    public_ids: List[str]

# Model for initializing delete article
class ArticleInit(BaseModel):
    article_id: int