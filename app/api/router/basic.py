from .base import *

router = APIRouter(
    prefix="/data",
    tags=["basic data"],
)


@router.get("/airports")
async def get_all_airports():
    return [
        AirportBody.transform(airport) 
        for airport in Airline.airports
    ]


@router.get("/aircraft/{model}}")
async def get_aircraft(model: str):
    aircraft = Airline.aircrafts.get(model)
    return AircraftBody.transform(aircraft)