from fastapi import FastAPI
from app.spawn import *

app = FastAPI()

@app.get("/", tags=['root'])
async def root() -> dict:
    return {"flight": "flights"}

@app.get("/flight", tags=['Flights'])
async def get_flights():
    return [
        {
            "designator": flight.designator,
            "departure": str(flight.departure),
            "arrival": str(flight.arrival),
            "origin": flight.origin.location_code,
            "destination": flight.destination.location_code,
        } for flight in Airline.flights
    ]

@app.post("/add_flight", tags=['Flights'])
async def create_flight(
    designator: str, 
    departure: str, 
    arrival: str, 
    origin: str,
    destination: str
) -> dict:
    flight1 = Flight(
        designator,
        time(*[
                int(x) for x in departure.split('_') # type: ignore
        ]),
        time(*[
                int(x) for x in arrival.split('_') # type: ignore
        ]),
        Airline.airports.search(origin)[0],
        Airline.airports.search(destination)[0],
    )
    Airline.flights.add(flight1)
    return {"Data": "create new flight successful."}

print(len(Airline.flights))

##from uvicorn import run
##run('app.api:app')