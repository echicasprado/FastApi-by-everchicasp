from sqlalchemy import Column, Integer, String
from database import Base

class EstadoModel(Base):
    __tablename__ = "TBL_ESTADO"

    id_estado = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, index=True)