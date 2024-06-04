from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
from config import get_db

from .shema import Area, AreaCreate
from .service import AreaServices

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
    areas = AreaServices.get_all_areas(db)

    if areas == None:
        return JSONResponse(content={"message":"No se puede obtener información"}, headers=HEADERS, status_code=500)

    content = [jsonable_encoder(area) for area in areas]
    header = HEADERS
    header["X-Total-Count"] = str(len(areas))
    return JSONResponse(content=content, headers=HEADERS)

@router.get("/get-areas", response_model=List[Area], status_code=200, description="Obtener todas las área disponibles", summary="Obtener todas las área disponibles")
async def get_areas(db: Session = Depends(get_db)):
    areas = AreaServices.get_available_areas(db)

    if areas == None:
        raise HTTPException(status_code=404, detail="No hay áreas disponibles")

    content = [jsonable_encoder(area) for area in areas]
    header = HEADERS
    header["X-Total-Count"] = str(len(areas))
    return JSONResponse(content=content, headers=HEADERS)

@router.get("/get-areas-by-parameters", response_model=List[Area], status_code=200, description="Obtener todas las área disponibles con argumentos", summary="Obtener todas las área disponibles con argumentos")
async def get_areas_sort(
    skip: int = Query(0,alias="skip", min = 0, max = 9),
    limit: int = Query(10, alias="limit", min = 2, max = 10),
    sort_by: str = Query("id_area", alias="sort_by"),
    order: str = Query("asc", alias="order", regex = "^(asc|desc)$", min_length = 3, max_length = 4), 
    db: Session = Depends(get_db)
    ):

    try:
        areas = AreaServices.get_area_by_parameters(db,skip,limit,sort_by,order)
        content = [jsonable_encoder(area) for area in areas]
        header = HEADERS
        header["X-Total-Count"] = str(len(areas))
        return JSONResponse(content=content, headers=HEADERS)
    except Exception as queryException:
        raise HTTPException(status_code=500, detail=str(queryException))

@router.get("/get-area/{id_area}", response_model=Area, status_code=200, description="Obtener área por el id")
async def get_area(id_area:int = Path(ge=1), db: Session = Depends(get_db)):
    area = AreaServices.get_area_by_id(db,id_area)
    
    if area is None:
        raise HTTPException(status_code=404, detail="Area no encontrada")
    
    return JSONResponse(content=jsonable_encoder(area), headers=HEADERS)

@router.get("/get-area-by-name/", response_model= Area, status_code=200, summary="Obtener área por nombre")
async def get_area_by_name(name:str = Query(min_length=1, max_length=100), db: Session = Depends(get_db)):
    area = AreaServices.get_area_by_descripcion(db,name)

    if area == None:
        raise HTTPException(status_code=404, detail="Area no encontrada")
    
    return JSONResponse(content=jsonable_encoder(area), headers=HEADERS)

@router.post("/create-area", response_model=Area, status_code=201, description="Crear una nueva área", summary="Crear una nueva área")
async def create_area(area:AreaCreate, db: Session = Depends(get_db)):
    db_area = AreaServices.create_area(db,area)

    if  db_area == None:
        raise HTTPException(status_code=404, detail="No se puede crear el área")

    return JSONResponse(content=jsonable_encoder(db_area), headers=HEADERS, status_code=201)

@router.patch("/update-area/{id_area}", response_model=Area, status_code=200, description="Actualizar área", summary="Actualizar área")
async def update_area(id_area:int, area:AreaCreate, db: Session = Depends(get_db)):
    db_area = AreaServices.update_area(db,id_area,area)

    if db_area is None:
        raise HTTPException(status_code=404,detail="Area no encontrada")
    
    return JSONResponse(content=jsonable_encoder(db_area), headers=HEADERS, status_code=200)
        
@router.delete("/delete-area/{id_area}", status_code=200, description="Eliminar área", summary="Eliminar área")
async def deleteArea(id_area:int = Path(...,ge=1), db: Session = Depends(get_db)):
    db_area = AreaServices.delete_area(db,id_area)

    if db_area is None:
        raise HTTPException(status_code=404,detail="Área no encontrada")
    
    return JSONResponse(content={"message":f"Área: {db_area.descripcion}, se ha eliminado con éxito"}, headers=HEADERS, status_code=200)