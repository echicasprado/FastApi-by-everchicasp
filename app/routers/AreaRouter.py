from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import List, Optional
from database import get_db

from models import AreaModel, EstadoModel
from shemas import Area, AreaCreate, EstadoEnum

HEADERS = {"Content-Type":"application/json","charset":"utf-8"}

router = APIRouter(
    prefix="/areas",
    tags= ["Areas"]
)

@router.get("/", status_code=200)
async def areas_home():
    content = {"message":"Areas - info projects"}
    return JSONResponse(content=content, headers= HEADERS)

@router.get("/get-areas-all", response_model=List[Area], status_code=200, description="Obtener todas las área", summary="Obtener todas las área")
async def get_areas(db: Session = Depends(get_db)):
    areas = db.query(AreaModel).all()

    if areas == None:
        return JSONResponse(content={"message":"No se puede obtener información"}, headers=HEADERS, status_code=500)

    for area in areas:
        area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == area.id_estado).first()

    content = [jsonable_encoder(area) for area in areas]
    header = HEADERS
    header["X-Total-Count"] = str(len(areas))
    return JSONResponse(content=content, headers=HEADERS)

@router.get("/get-areas", response_model=List[Area], status_code=200, description="Obtener todas las área disponibles", summary="Obtener todas las área disponibles")
async def get_areas(db: Session = Depends(get_db)):
    areas = db.query(AreaModel).filter(AreaModel.id_estado == EstadoEnum.ACTIVO).all()

    if areas == None:
        raise HTTPException(status_code=404, detail="No hay áreas disponibles")

    for area in areas:
        area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == area.id_estado).first()
    
    content = [jsonable_encoder(area) for area in areas]
    header = HEADERS
    header["X-Total-Count"] = str(len(areas))
    return JSONResponse(content=content, headers=HEADERS)

# TODO buscar error, muestra que order_by_column no puede ser un list
@router.get("/get-areas-by", response_model=List[Area], status_code=200, description="Obtener todas las área disponibles con argumentos", summary="Obtener todas las área disponibles con argumentos")
async def get_areas_sort(
    skip: Optional[int] = Query(1,alias="skip", min = 1, max = 9),
    limit: Optional[int] = Query(10, alias="limit", min = 2, max = 10),
    sort_by: Optional[str] = Query("id_area", alias="sort_by"),
    order: Optional[str] = Query("asc", alias="order", regex = "^(asc|desc)$", min_length = 3, max_length = 4), 
    db: Session = Depends(get_db)
    ):
    
    query = db.query(AreaModel).filter(AreaModel.id_estado == EstadoEnum.ACTIVO).all()
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
        
        for area in areas:
            area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == area.id_estado).first()

        content = [jsonable_encoder(area) for area in areas]
        header = HEADERS
        header["X-Total-Count"] = str(len(areas))

    except Exception as queryException:
        raise HTTPException(status_code=500, detail=str(queryException))
    
    return JSONResponse(content=content, headers=HEADERS)

# TODO realizar busqueda por estado y por id
@router.get("/get-area/{id_area}", response_model=Area, status_code=200, description="Obtener área por el id")
async def get_area(id_area:int = Path(ge=1), db: Session = Depends(get_db)):
    area = db.query(AreaModel).filter(AreaModel.id_area == id_area).first()
    
    if area is None:
        raise HTTPException(status_code=404, detail="Area no encontrada")
    
    area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == area.id_estado).first()
    return JSONResponse(content=jsonable_encoder(area), headers=HEADERS)

# TODO realizar busqueda por estado y por nombre
@router.get("/get-area-by-name/", response_model= Area, status_code=200, summary="Obtener área por nombre")
async def get_area_by_name(name:str = Query(min_length=1, max_length=100), db: Session = Depends(get_db)):
    area = db.query(AreaModel).filter(AreaModel.descripcion == name).first()

    if area == None:
        raise HTTPException(status_code=404, detail="Area no encontrada")
    
    area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == area.id_estado).first()
    return JSONResponse(content=jsonable_encoder(area), headers=HEADERS)

@router.post("/create-area", response_model=Area, status_code=201, description="Crear una nueva área", summary="Crear una nueva área")
async def create_area(area:AreaCreate, db: Session = Depends(get_db)):
    db_area = AreaModel(descripcion = area.descripcion, id_estado = EstadoEnum.ACTIVO)
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    db_area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == db_area.id_estado).first()
    return JSONResponse(content=jsonable_encoder(db_area), headers=HEADERS, status_code=201)

# TODO realizar busqueda por estado y por id
@router.patch("/update-area/{id_area}", response_model=Area, status_code=200, description="Actualizar área", summary="Actualizar área")
async def update_area(id_area:int, area:AreaCreate, db: Session = Depends(get_db)):
    db_area = db.query(AreaModel).filter(AreaModel.id_area == id_area).first()

    if db_area is None:
        raise HTTPException(status_code=404,detail="Area no encontrada")
    
    db_area.descripcion = area.descripcion
    db_area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == db_area.id_estado).first()
    db.commit()
    db.refresh(db_area)
    db_area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == db_area.id_estado).first()
    return JSONResponse(content=jsonable_encoder(db_area), headers=HEADERS, status_code=200)
        
# TODO realizar busqueda por estado y por id
@router.delete("/delete-area/{id_area}", status_code=200, description="Eliminar área", summary="Eliminar área")
async def deleteArea(id_area:int = Path(...,ge=1), db: Session = Depends(get_db)):
    db_area = db.query(AreaModel).filter_by(id_estado = EstadoEnum.ACTIVO, id_area = id_area).first()

    if db_area is None:
        raise HTTPException(status_code=404,detail="Área no encontrada")
    
    db_area.id_estado = EstadoEnum.INACTIVO
    db.commit()
    db.refresh(db_area)
    db_area.estado = db.query(EstadoModel).filter(EstadoModel.id_estado == db_area.id_estado).first()
    return JSONResponse(content={"message":f"Área: {db_area.descripcion}, se ha eliminado con éxito"}, headers=HEADERS, status_code=200)