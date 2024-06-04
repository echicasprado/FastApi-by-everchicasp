from pydantic import BaseModel
from typing import Optional

from modules.estado import Estado

class AreaBase(BaseModel):
    descripcion: str

class AreaCreate(AreaBase):
    pass

class Area(AreaBase):
    id_area: int
    estado: Optional[Estado]

    class Config:
        orm_mode = True