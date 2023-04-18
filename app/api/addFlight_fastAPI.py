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
            "origin": flight.origin.location_code,
            "destination": flight.destination.location_code,
        } for flight in Airline.flights
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
        Airline.airports.get(origin),
        Airline.airports.get(destination),
    )
    Airline.flights.append(flight1)
    return {"Data": "create new flight successful."}

print(len(Airline.flights))