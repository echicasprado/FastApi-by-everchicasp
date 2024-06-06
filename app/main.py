from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules import *
from middleware import ErrorHandler

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:60427"
]

app = FastAPI(
    title="Info projects API",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandler)


app.include_router(jwt_router)
app.include_router(estado_router)
app.include_router(area_router)