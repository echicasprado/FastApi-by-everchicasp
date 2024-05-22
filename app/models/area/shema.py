from pydantic import BaseModel

class AreaBase(BaseModel):
    descripcion: str
    id_estado:int

class AreaCreate(BaseModel):
    descripcion: str

class Area(AreaBase):
    id_area: int

    class Config:
        orm_mode = True