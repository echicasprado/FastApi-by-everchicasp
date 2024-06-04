from pydantic import BaseModel
from enum import Enum

class EstadoEnum(str,Enum):
    ACTIVO = 1
    INACTIVO = 2

class EstadoBase(BaseModel):
    descripcion: str

class EstadoCreate(BaseModel):
    pass

class Estado(EstadoBase):
    id_estado: int

    class Config:
        orm_mode = True