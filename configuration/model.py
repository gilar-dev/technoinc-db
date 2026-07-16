from pydantic import BaseModel
from typing import List, Dict, Any

# Model for initializing upload article
class WikiArticlePayload(BaseModel):
    id: str
    title: str
    category: str
    cover: str
    public_id: str
    visited: int = 0
    wiki_content: List[Dict[str, Any]]

# Model for initializing update article
class WikiArticleUpdate(BaseModel):
    id: str
    wiki_content: List[Dict[str, Any]]

# Model for getting assets public id
class ImagePublicId(BaseModel):
    public_ids: List[str]

# Model for initializing delete article
class ArticleInit(BaseModel):
    id: str
    category: str