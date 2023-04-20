"""
https://fastapi.tiangolo.com/tutorial/bigger-applications

"""
from .base import *
from .router import *
import app.spawn

from . import addFlight_fastAPI, login_fastAPI, registor_fastAPI

web = FastAPI()

for module in (
    get_data,
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


##from uvicorn import run
##run('app.api:app')