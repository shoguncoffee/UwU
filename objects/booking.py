"""
"""
from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from seat import Seat
    from person import Passenger

STATUS = Enum(
    'Booking Status', 
    'PAID CHECKIN'
)

@dataslots
class Booking:
    passenger: Passenger
    seats: list[Seat]
    status: STATUS
    
    
if __name__ != '__main__':
    globals().update(STATUS.__members__)