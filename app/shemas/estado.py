from pydantic import BaseModel

class EstadoBase(BaseModel):
    descripcion: str

class EstadoCreate(BaseModel):
    pass

class Estado(EstadoBase):
    id_estado: int

    class Config:
        orm_mode = True