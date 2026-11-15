from pydantic import BaseModel
from typing import Literal

type Classification = Literal["start", "ga", "fa"]
type EditPermission = Literal["free", "strict"]

class RevisionHistory(BaseModel):
    sts: Literal["create", "edit"] # Modification status
    user: str # User / contributor name
    sum: str # Modification summary
    date: str # Modification date
    m_logs: list[str] # Modification block list

# Article wiki frame model
class ArticleModel(BaseModel):
    title: str # Article title
    id: int # Article unique id
    ver: int # Article version
    view: int # Article view
    desc: str # Article brief description
    cover: str # Article cover url
    p_id: str # Article cover public id
    cls: Classification # Article classification
    cat: list[str] # Article category list
    edit: EditPermission # Article edit permission status
    his: list[RevisionHistory] # Article revision history list
    content: None