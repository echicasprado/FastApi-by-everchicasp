from sqlalchemy.orm import Session
from typing import List
from .model import EstadoModel
from .shema import Estado

class EstadoServices():

    def get_estados(db:Session) -> List[Estado]:
        return db.query(EstadoModel).all()
    
    