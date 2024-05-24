from sqlalchemy.orm import Session
from typing import List
from models import EstadoModel
from shemas import Estado

class EstadoServices():
    
    def get_estados(db: Session) -> List[Estado]:
        return db.query(EstadoModel).all()
    
    