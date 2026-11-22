from pydantic import BaseModel
from typing import Literal

class ErrorModel(BaseModel):
    status: Literal["Error"]
    message: str