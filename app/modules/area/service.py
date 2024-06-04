from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import List

from modules.estado import EstadoEnum, EstadoModel
from .model import AreaModel
from .shema import Area, AreaCreate

class AreaServices():

    def get_all_areas(db: Session) -> List[Area]:
        areas = db.query(AreaModel).all()

        for area in areas:
            area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == area.id_estado).first()

        return areas
    
    def get_available_areas(db:Session) -> List[Area]:
        areas = db.query(AreaModel).filter(AreaModel.id_estado == EstadoEnum.ACTIVO).all()

        for area in areas:
            area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == area.id_estado).first()

        return areas
    
    def get_area_by_parameters(db:Session, skip:int, limit:int, sort_by:str, order:str)->List[AreaModel]:
        query = db.query(AreaModel).filter(AreaModel.id_estado == EstadoEnum.ACTIVO)
        order_by_column = getattr(AreaModel,sort_by)
        
        if order == "desc":
            query = query.order_by(desc(order_by_column))
        else:
            query = query.order_by(asc(order_by_column))
        
        areas = query.offset(skip).limit(limit).all()
    
        for area in areas:
            area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == area.id_estado).first()

        return areas

    def get_area_by_id(db:Session, id_area:int) -> Area:
        area = db.query(AreaModel).filter_by(id_estado = EstadoEnum.ACTIVO, id_area = id_area).first()

        if area != None:
            area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == area.id_estado).first()
        
        return area
    
    def get_area_by_descripcion(db:Session, descripcion:str) -> Area:
        area = db.query(AreaModel).filter_by(id_estado = EstadoEnum.ACTIVO, descripcion = descripcion).first()

        if area != None:
            area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == area.id_estado).first()
        
        return area
    
    def create_area(db:Session, area:AreaCreate) -> Area:
        db_area = AreaModel(descripcion = area.descripcion, id_estado = EstadoEnum.ACTIVO)
        db.add(db_area)
        db.commit()
        db.refresh(db_area)
        db_area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == db_area.id_estado).first()
        return db_area
    
    def update_area(db:Session, id_area:int, area:AreaCreate) -> Area:
        db_area = db.query(AreaModel).filter_by(id_estado = EstadoEnum.ACTIVO, id_area = id_area).first()

        if db_area != None:
            db_area.descripcion = area.descripcion
            db.commit()
            db.refresh(db_area)
            db_area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == db_area.id_estado).first()
        
        return db_area
    
    def delete_area(db:Session, id_area:int) -> Area:
        db_area = db.query(AreaModel).filter_by(id_estado = EstadoEnum.ACTIVO, id_area = id_area).first()

        if db_area != None:
            db_area.id_estado = EstadoEnum.INACTIVO
            db.commit()
            db.refresh(db_area)
            db_area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == db_area.id_estado).first()

        return db_area
