from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.responses import HTMLResponse
from typing import List, Optional
from models.area.model import Area as AreaModel
from models.area.shema import Area, AreaCreate
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import asc, desc

router = APIRouter(
    prefix="/areas",
    tags= ["Areas"]
)

@router.get("/", status_code=200)
def areas_home():
    return HTMLResponse("<h1>Areas - info projects</h1>")

@router.get("/get-areas-all", response_model=List[Area], status_code=200, description="Obtener todas las área", summary="Obtener todas las área")
def get_areas(db: Session = Depends(get_db)):
    areas = db.query(AreaModel).all()
    return areas

@router.get("/get-areas", response_model=List[Area], status_code=200, description="Obtener todas las área disponibles", summary="Obtener todas las área disponibles")
def get_areas(db: Session = Depends(get_db)):
    areas = db.query(AreaModel).filter(AreaModel.id_estado == 1).all()
    if areas == None:
        raise HTTPException(status_code=404, detail="No hay áreas disponibles")
    return areas

@router.get("/get-areas-by", response_model=List[Area], status_code=200, description="Obtener todas las área disponibles con argumentos", summary="Obtener todas las área disponibles con argumentos")
def get_areas_sort(
    skip: Optional[int] = Query(1,alias="skip", min = 1, max = 9),
    limit: Optional[int] = Query(10, alias="limit", min = 2, max = 10),
    sort_by: Optional[str] = Query("id_area", alias="sort_by"),
    order: Optional[str] = Query("asc", alias="order", regex = "^(asc|desc)$", min_length = 3, max_length = 4), 
    db: Session = Depends(get_db)
    ):
    
    query = db.query(AreaModel)
    order_by_column = getattr(AreaModel, sort_by)

    if order == "desc":
        query = query.order_by(desc(order_by_column))
    else:
        query = query.order_by(asc(order_by_column))

    query = query.offset(skip).limit(limit)

    try:
        areas = query.all()
        if areas == None:
            raise HTTPException(status_code=404, detail="Area no encontrada")
    except Exception as queryException:
        raise HTTPException(status_code=500, detail=str(queryException))
    
    return areas


@router.get("/get-area/{id_area}", response_model=Area, status_code=200, description="Obtener área por el id")
def get_area(id_area:int = Path(ge=1), db: Session = Depends(get_db)) -> Area:
    area = db.query(AreaModel).filter(AreaModel.id_area == id_area).first()
    if area is None:
        raise HTTPException(status_code=404, detail="Area no encontrada")
    return area

@router.get("/get-area-by-name/", response_model= Area, status_code=200, summary="Obtener área por nombre")
def get_area_by_name(name:str = Query(min_length=1, max_length=100), db: Session = Depends(get_db)):
    area = db.query(AreaModel).filter(AreaModel.descripcion == name).first()
    if area == None:
        raise HTTPException(status_code=404, detail="Area no encontrada")
    return area

@router.post("/create-area", response_model=Area, status_code=201, description="Crear una nueva área", summary="Crear una nueva área")
def create_area(area:AreaCreate, db: Session = Depends(get_db)) -> Area:
    db_area = AreaModel(descripcion = area.descripcion)
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

@router.patch("/update-area/{id_area}", response_model=Area, status_code=200, description="Actualizar área", summary="Actualizar área")
def update_area(id_area:int, area:AreaCreate, db: Session = Depends(get_db)):
    db_area = db.query(AreaModel).filter(AreaModel.id_area == id_area).first()

    if db_area is None:
        raise HTTPException(status_code=404,detail="Area no encontrada")
    
    db_area.descripcion = area.descripcion
    db.commit()
    db.refresh(db_area)
    return db_area
        
@router.delete("/delete-area/{id_area}", status_code=200, description="Eliminar área", summary="Eliminar área")
def deleteArea(id_area:int = Path(ge=1), db: Session = Depends(get_db)):
    db_area = db.query(AreaModel).filter(AreaModel.id_area == id_area).first()

    if db_area is None:
        raise HTTPException(status_code=404,detail="Area no encontrada")
    
    db_area.id_estado = 2
    db.commit()
    db.refresh(db_area)
    return db_area