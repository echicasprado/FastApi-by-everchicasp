from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from typing import List
from models.area.shema import Area, AreaGet, AreaPost, AreaUpdate, AreaDelete
 
FAKE = [
    Area(id=1, description="Area 1", available=True),
    Area(id=2, description="Area 2", available=False),
    Area(id=3, description="Area 3", available=True),
]


router = APIRouter(
    prefix="/areas",
    tags= ["Areas"]
)

@router.get("/", status_code=200)
def areas_home():
    return HTMLResponse("<h1>Areas info projects</h1>")

@router.get("/get-areas", response_model=List[Area], status_code=200)
def getAreas():
    return FAKE

@router.post("/create-area", response_model=AreaGet, status_code=201)
def createNewArea(area:AreaPost) -> AreaGet:
    newArea = Area(id=len(FAKE) + 1, description=area.description,available=True)
    FAKE.append(newArea)
    return newArea

@router.patch("update-area",response_model=AreaGet, status_code=200)
def updateArea(areaUpdate:AreaUpdate):
    for area in FAKE:
        if area.id == areaUpdate.id:
            area.description = areaUpdate.description
            return area
        
@router.delete("delete-area", status_code=200)
def deleteArea(areaDelete: AreaDelete):
    for area in FAKE:
        if area.id == areaDelete.id:
            area.available = False
            return HTMLResponse("Operación exitosa")