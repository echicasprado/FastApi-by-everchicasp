from fastapi import FastAPI
from routers import *
from fastapi.middleware.cors import CORSMiddleware

BASE_URL="info-projects"

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


app.include_router(area_router)