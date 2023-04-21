"""
https://docs.python.org/3/library/enum.html
https://docs.python.org/3/howto/enum.html#functional-api
https://fastapi.tiangolo.com/sq/tutorial/path-params/#working-with-python-enumerations

enum constants
function-call syntax
"""
from typing import Type as _Type
from enum import (
    IntEnum as _Enum, 
    StrEnum as _StrEnum
)

FlightStatus = _Enum(
    'FlightStatus', 'SCHEDULED CANCELLED IN_FLIGHT ARRIVED'
)
PassengerType = _Enum(
    'PassengerType', 'ADULT CHILD INFANT'
)

# must sort by priority
TravelClass = _Enum(
    'TravelClass', 'ECONOMY BUSSINESS FIRST'
)
AccountStatus = _Enum(
    'AccountStatus', 'PENDING ACTIVE SUSPENDED INACTIVE'
)
BookingStatus = _Enum(
    'BookingStatus', 'FAILED INCOMPLETE PENDING COMPLETED CANCELLED'
)
SeatType = _Enum(
    'SeatType', 'LEGROOM WINDOW AISLE COMMON'
)
GenderType = _Enum(
    'GenderType', 'MALE FEMALE'
)
PaymentStatus = _Enum(
    'PaymentStatus', 'PENDING FAILED COMPLETED'
)
PaymentMethod = _Enum(
    'PaymentMethod', 'PAYPAL INTERNET_BANKING CREDIT_CARD'
)

with open('data/countries.txt') as _f:
    Country: _Type[_StrEnum] = _StrEnum(
        'Country', _f.read().splitlines()
    )