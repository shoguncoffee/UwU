"""
"""
from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from aircraft import Aircraft
    from airport import Airport
    from seat import Seat

STATUS = Enum('Flight Status', 
    'SCHEDULED IN_FLIGHT ARRIVED CANCLE DELAY'
)

@dataslots
class Flight:
    number: str
    aircraft: Aircraft
    gate: str
    origin: Airport
    destination: Airport
    departure_time: datetime
    arrival_time: datetime
    seats: list[Seat]
    status: STATUS = STATUS.SCHEDULED
        
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
    ...
    #Flight(status=Status.CANCLE)