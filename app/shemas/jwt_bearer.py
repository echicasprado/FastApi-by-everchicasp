from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from middleware import validate_token

class JWT_Bearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['correo'] != "admin@example.com":
            raise(HTTPException(status_code=403, detail="Credenciales invalidas"))