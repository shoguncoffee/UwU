"""
https://docs.python.org/3/library/enum.html
https://docs.python.org/3/howto/enum.html#functional-api
https://fastapi.tiangolo.com/sq/tutorial/path-params/#working-with-python-enumerations

function-call syntax
first argument must match the name
"""
from enum import IntEnum, IntFlag, StrEnum


FlightStatus = IntEnum(
    'FlightStatus', (
        'SCHEDULED', 
        'CANCELLED', 
        'IN_FLIGHT', 
        'ARRIVED',
    )
)
PassengerType = IntEnum(
    'PassengerType', (
        'ADULT', 
        'CHILD', 
        'INFANT',
    )
)
# must sort by priority
TravelClass = IntEnum(
    'TravelClass', (
        'ECONOMY', 
        'BUSSINESS', 
        'FIRST',
    )
)
AccountStatus = IntEnum(
    'AccountStatus', (
        'ACTIVE', 
        'SUSPENDED', 
        'INACTIVE',
    )
)
BookingStatus = IntEnum(
    'BookingStatus', (
        'INCOMPLETE', 
        'FAILED', 
        'PENDING', 
        'CANCELLED',
        'COMPLETED', 
    )
)
SeatType = IntFlag(
    'SeatType', (
        'COMMON', 
        'AISLE', 
        'WINDOW', 
        'LEGROOM',
    )
)
GenderType = IntEnum(
    'GenderType', (
        'MALE', 
        'FEMALE',
    )
)
with open('data/countries.txt') as _f:
    Country = StrEnum(
        'Country', _f.read().splitlines()
    )