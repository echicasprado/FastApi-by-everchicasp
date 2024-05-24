from pydantic import BaseModel
from typing import Optional
from .estado import Estado

class AreaBase(BaseModel):
    descripcion: str

class AreaCreate(BaseModel):
    pass

class Area(AreaBase):
    id_area: int
    estado: Optional[Estado]

    class Config:
        orm_mode = True