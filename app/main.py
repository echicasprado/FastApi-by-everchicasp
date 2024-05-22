from fastapi import FastAPI
from routers import AreaRouter

BASE_URL="info-projects"

app = FastAPI(
    title="Info projects API",
    version="0.0.1"
)

app.include_router(AreaRouter.router)