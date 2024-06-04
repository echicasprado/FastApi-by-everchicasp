from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
from config import get_db

from .shema import Estado
from .service import EstadoServices

HEADERS = {"Content-Type":"application/json","charset":"utf-8"}

router = APIRouter(
    prefix="/estado",
    tags= ["Estado"]
)

@router.get("/", status_code=200)
async def estado_home():
    content = {"message":"Estado - info projects"}
    return JSONResponse(content=content,headers=HEADERS,status_code=200)

@router.get("/get-estados", response_model=List[Estado], status_code=200, description="Retornar los estados validos", summary="Retornar los estados validos")
async def get_estados(db: Session = Depends(get_db)):
    estados = EstadoServices.get_estados(db)

    if estados == None:
        return JSONResponse(content={"message":"No se encuentra información"},headers=HEADERS,status_code=500)

    content = [jsonable_encoder(estado) for estado in estados]
    header = HEADERS
    header["X-Total-Count"] = str(len(estados))
    return JSONResponse(content=content,headers=HEADERS,status_code=200)
