from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config import Base

class EstadoModel(Base):
    __tablename__ = "TBL_ESTADO"

    id_estado = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, index=True)

    areas = relationship("AreaModel", order_by="AreaModel.id_area", back_populates="estado")