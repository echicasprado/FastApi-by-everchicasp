from pydantic import BaseModel

class EstadoBase(BaseModel):
    descripcion: str

class EstadoCreate(BaseModel):
    descripcion: str

class Estado(EstadoBase):
    pass 

    class Config:
        orm_mode = True