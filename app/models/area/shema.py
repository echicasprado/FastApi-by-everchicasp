from pydantic import BaseModel, Field
from typing import Optional

class AreaBase(BaseModel):
    description: str = Field(min_length=5, max_length=20)
    available:bool

class Area(AreaBase):
    id: int

class AreaGet(Area):
    pass

class AreaPost(BaseModel):
    description: str = Field(default="Nueva area", min_length=5, max_length=20)

class AreaUpdate(BaseModel):
    id: int
    description: Optional[str] = None
    available: Optional[bool] = None

class AreaDelete(BaseModel):
    id: int