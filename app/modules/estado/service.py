from sqlalchemy.orm import Session
from typing import List
from .model import EstadoModel
from .shema import Estado

class EstadoServices():

    def __init__(self, db) -> None:
        self.db = db
    
    def get_estados(self) -> List[Estado]:
        return self.db.query(EstadoModel).all()
    
    