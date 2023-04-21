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
):
    web.include_router(module.router)


@web.get("/")
async def root():
    return 'Hello'


import app.spawn