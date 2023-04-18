"""
https://fastapi.tiangolo.com/tutorial/bigger-applications

"""
from .base import *
from .router import *
import app.spawn

web = FastAPI()

for module in (
    get_data,
    search_flight,
    user,
    booking,
    payment,
):
    web.include_router(module.router)


@web.get("/")
async def root():
    return 'Hello'

