from typing import Annotated
from fastapi import FastAPI, Query, Depends, APIRouter
from pydantic import BaseModel
import datetime
from dataclasses import dataclass

app = FastAPI()

class Date(BaseModel):
    date: datetime.date | str
    
    
from enum import Enum, IntEnum, StrEnum

PassengerType = Enum(
    'PassengerType', 'ADULT CHILD INFANT'
)
GenderType = Enum(
    'GenderType', 'MALE FEMALE'
)
Gender1 = StrEnum(
    'GenderType1', 'MALE FEMALE'
)
Gender2 = IntEnum(
    'GenderType2', 'MALE FEMALE'
)

async def common_parameters(
    q: str | None = None, 
    skip: int = 0, 
    limit: int = 100
):
    return 10


@app.get("/items/")
async def read_items(q: int, commons: Annotated[dict, Depends(common_parameters)]):
    return q, commons

@app.get("/users/")
async def read_users(q: str, commons: Annotated[dict, Depends(common_parameters)]):
    return q, commons


router = APIRouter(
    prefix="/depend",
    tags=["depend"],
    dependencies=[Depends(common_parameters)],
)

@router.get("/users")
async def read_users2(q: str):
    return q

app.include_router(router)


class PassengerDetails(BaseModel):
    forename: str # type: ignore
    surname: str # type: ignore
    birthdate: datetime.date # type: ignore
    nationality: str # type: ignore
    passport_id: str # type: ignore
    gender: GenderType # type: ignore
    passenger_type: PassengerType # type: ignore
    
    @property
    def fullname(self):
        return f'{self.forename} {self.surname}'


@app.post('/')
async def root(
    passengers: list[PassengerDetails], 
    date: list[tuple[datetime.date, str]]
):
    return passengers, date

@app.get('/a')
async def root2(date: datetime.date):
    return {"Hello": repr(date)}

@app.get('/t')
async def test(
    q: list[int] = Query(), 
    e: tuple[int, int] = Query()
):
    return [repr(q), repr(e)]

@app.get('/s')
async def root3(gender: GenderType):
    return gender

@app.get('/d')
async def root4(gender: Gender1):
    return gender

@app.get('/f')
def root5(gender: Gender2):
    return gender


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('api:app', reload=True)