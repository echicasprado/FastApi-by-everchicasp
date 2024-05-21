from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from typing import List
from ..models.area.shema import Area, AreaGet, AreaPost, AreaUpdate, AreaDelete

DB_FAKE = [
    Area(id=1,description="Area 1", available=True),
    Area(id=2,description="Area 2", available=True),
    Area(id=3,description="Area 3", available=True)
]

router = APIRouter(
    prefix= "/areas",
    tags= ["Areas"]
)

@router.get("/", status_code=200)
def area_home():
    return HTMLResponse("<h1> Areas info projects</h1>")