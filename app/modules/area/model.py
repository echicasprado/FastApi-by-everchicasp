from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

from modules.estado import EstadoModel

class AreaModel(Base):
    __tablename__ = "TBL_AREA"

    id_area = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, index=True)
    id_estado = Column(Integer, ForeignKey("TBL_ESTADO.id_estado"))

    estado = relationship("EstadoModel", back_populates="areas")