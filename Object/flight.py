from base import *
from aircraft import Aircraft

@dataclass
class Flight:
    ID: str
    aircraft: Aircraft
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    status = ...
    
    def __post_init__(self):
        ...
    
    @property
    def travel_time():
        return 
    
    @property
    def 
    
    
# status -> SCHEDULED, 