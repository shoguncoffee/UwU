"""
"""
from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from seat import Seat
    from person import Passenger
    
Status = Enum(
    'Booking Status', 
    'UNPAID PAID CHECKIN'
)

@dataclass
class Booking:
    id: str
    passenger: Passenger
    seats: Seat
    status: Status = Status.UNPAID
    
    
if __name__ != '__main__':
    globals().update(Status.__members__)