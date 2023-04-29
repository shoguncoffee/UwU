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
    payment,
    addFlight_fastAPI,
    login_fastAPI,
    registor_fastAPI
):
    web.include_router(module.router)


@web.get("/")
async def root():
    return 'Hello'


from app.system import Airline
Airline.load()
