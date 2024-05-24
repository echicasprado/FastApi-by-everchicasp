from sqlalchemy import Column, Integer, String
from database import Base

class AreaModel(Base):
    __tablename__ = "TBL_AREA"

    id_area = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, index=True)
    id_estado = Column(Integer, default=True)