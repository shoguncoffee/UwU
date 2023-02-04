from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from aircraft import Aircraft
    from airport import Airport
    from seat import Seat

Status = Enum('Flight Status', 
    'SCHEDULED CANCLE'
)

@dataclass
class Flight:
    code: str
    aircraft: Aircraft
    origin: Airport
    destination: Airport
    departure: datetime
    arrival: datetime
    seats: list[Seat]
    status: Status = Status.SCHEDULED
        
    
    def __post_init__(self):
        ...
    
    @property
    def travel_time(self):
        return 
    
    @property
    def passenger(self):
        return sum()
   
    @property
    def estimated_time(self):  
        return self.arrival - self.departure
    
    
if __name__ != '__main__':
    #globals().update()
    Flight(status=Status.CANCLE)