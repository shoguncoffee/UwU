from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from aircraft import Aircraft
    from airport import Airport
    from seat import Seat


@dataclass
class Flight:
    code: str
    aircraft: Aircraft
    origin: Airport
    destination: Airport
    departure: datetime
    arrival: datetime
    seats: list[Seat]
    status: STATUS
    
    STATUS = Enum('Flight Status', 
        'SCHEDULED CANCLE'
    )
    
    
    def __post_init__(self):
        ...
    
    @property
    def travel_time(self):
        return 
    
    @property
    def passenger(self):
        return sum()
   

Flight.
if __name__ != '__main__':
    globals().update(STATUS.__members__)
    