from pydantic import BaseModel
from typing import Literal
from .block_model import Block

type Classification = Literal["start", "ga", "fa"]
type EditPermission = Literal["free", "strict"]
type ModificationLogs = list[tuple[Literal["add", "move", "delete"], str]]

class RevisionHistory(BaseModel):
    sts: Literal["create", "edit"] # Modification status
    user: str # User / contributor name
    sum: str # Modification summary
    date: str # Modification date
    m_logs: ModificationLogs # Modification block list

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
    content: list[Block]

class Basicinfo(BaseModel):
    title: str
    content_length: int
    id: int
    view: int
    description: str
    cover: str

class EditHistory(BaseModel):
    creator: str
    creation_date: str
    latest_editor: str
    latest_edit_date: str
    total_edit: int

class Property(BaseModel):
    categories: list[str]

class ArticleInformationData(BaseModel):
    basic_info: Basicinfo
    edit_history: EditHistory
    property: Property

class ArticleInformationModel(BaseModel):
    status: Literal["Success", "Error"]
    data: ArticleInformationData