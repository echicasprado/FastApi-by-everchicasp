from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from shemas import Usuario, JWT_Bearer
from middleware import create_token

router = APIRouter(
    prefix="/autenticacion",
    tags= ["Autenticacion"]
)

@router.post("/login")
async def login(user:Usuario):
    if(user.correo=="admin@example.com" and user.password=="1234"):
        return JSONResponse(content=create_token(user.dict()), status_code=200)
    else:
        return JSONResponse(content="Error en autenticación", status_code=400)
    
@router.get("/info", dependencies=[Depends(JWT_Bearer())])
async def get_info_user():
    return JSONResponse(content={"message":"info"}, status_code=200)
