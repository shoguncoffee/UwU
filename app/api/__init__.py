"""
https://fastapi.tiangolo.com/tutorial/bigger-applications
"""
from .base import *
from .router import *


web = FastAPI()

for module in (
    basic,
    search_flight,
    user,
    booking,
    addFlight_fastAPI,
    login_fastAPI,
    registor_fastAPI
):
    web.include_router(module.router)


@web.get("/")
async def root():
    return 'Hello'


@web.get("/avaliable-seat")
async def get_avaliable_seat(
    date: dt.date,
    designator: str,
    travel_class: TravelClass,
):
    schedule = system.schedules.get(date)
    flight_instance = schedule.get(designator)
    remaining = flight_instance.get_class(travel_class).get_remain_seats()
    
    return [
        seat.number for seat in sorted(remaining)
    ]