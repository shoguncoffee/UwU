from .base import *

router = APIRouter(
    prefix="/data",
    tags=["basic data"],
)


@router.get("/airports")
async def get_all_airports():
    return [
        AirportBody.transform(airport) 
        for airport in system.airports
    ]


@router.get("/aircraft/{model}}")
async def get_aircraft(model: str):
    aircraft = system.aircrafts.get(model)
    return AircraftBody.transform(aircraft)


@router.get("/aircrafts")
async def get_all_aircraft():
    return {
        aircraft.model: AircraftBody.transform(aircraft)
        for aircraft in system.aircrafts
    }