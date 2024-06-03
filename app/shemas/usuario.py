from pydantic import BaseModel, Field

class Usuario(BaseModel):
    correo: str
    password: str = Field(min_length=4)