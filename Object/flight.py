from base import *
from aircraft import Aircraft
from airport import Airport

@dataclass
class Flight:
    code: str
    aircraft: Aircraft
    origin: Airport
    destination: Airport
    departure: datetime
    arrival: datetime
    status = ...
    
    def __post_init__(self):
        ...
    
    @property
    def travel_time(self):
        return 
    
    @property
    def 
    
    
# status -> SCHEDULED, 