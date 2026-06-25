from pydantic import BaseModel
from typing import List, Dict, Any

class WikiArticlePayload(BaseModel):
    id: str
    title: str
    category: str
    cover: str
    visited: int = 0
    wiki_content: List[Dict[str, Any]]