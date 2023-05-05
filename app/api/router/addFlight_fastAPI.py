from .base import *

router = APIRouter(
    prefix='/flight',
    tags=["addFlight"],
)

@router.get("/get_flight")
async def get_flights():
    return [
        {
            "designator": flight.designator,
            "departure": flight.departure,
            "arrival": flight.arrival,
            "origin": flight.origin.code,
            "destination": flight.destination.code,
        } for flight in system.flights
    ]

@router.post("/add_flight")
async def create_flight(
    designator: str, 
    departure: dt.time, 
    arrival: dt.time, 
    origin: str,
    destination: str
) -> dict:
    flight1 = src.Flight(
        designator,
        departure,
        arrival,
        system.airports.get(origin),
        system.airports.get(destination),
    )
    system.flights.add(flight1)
    return {"Data": "create new flight successful."}