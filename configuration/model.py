from fastapi import UploadFile
from pydantic import BaseModel
from typing import List, Dict, Any

# Model for initializing upload article
class WikiArticlePayload(BaseModel):
    title: str
    id: int
    ver: int
    desc: str
    cover: str
    p_id: str
    view: int
    cls: str
    cat: str
    edit: str
    his: str
    content: str

# Model for initializing update article
class WikiArticleUpdate(BaseModel):
    id: int
    wiki_content: List[Dict[str, Any]]

# Model for creating new wiki category
class WikiCreateCategory(BaseModel):
    category_name: str
    category_parent: str

# Model for getting assets public id
class ImagePublicId(BaseModel):
    folder_name: str
    public_ids: List[str]
    delete_folder: bool = False

class ImageFormData(BaseModel):
    form_data_list: List[UploadFile]

# Model for initializing delete article
class ArticleInit(BaseModel):
    article_id: int

# Model for checking all available articles
class LinkCheckRequest(BaseModel):
    links: List[str]