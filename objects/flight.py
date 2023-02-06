"""
"""
from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from aircraft import Aircraft
    from airport import Airport
    from seat import Seat

Status = Enum('Flight Status', 
    'SCHEDULED IN_FLIGHT ARRIVED'
)

@dataclass
class FlightManager:
    """
    manipulate a flight
    """
    fligt: list[Flight]
    flight_generater: FlightGenerater = ...
    
    def create_flight(self):
        ...
        

class FlightGenerater:
    @classmethod
    def generate_flight():
        ...
        
    @classmethod
    def generate_designator():
        ...


@dataclass
class FlightService:
    """
    
    """
    reservation: list[Seat]
    status: Status = Status.SCHEDULED
    
    def __post_init__(self):
        ...
        
    @property
    def passenger(self):
        return len(self.reservation)

@dataclass
class Flight:
    """
    contain all information about a flight
    """
    aircraft: Aircraft
    designator: FlightDesignator
    origin: Airport
    destination: Airport
    departure_time: datetime
    arrival_time: datetime
    
    @property
    def travel_time(self):
        return 
    
   
    @property
    def duration(self):  
        return self.arrival_time - self.departure_time


@dataclass
class FlightDesignator:
    """
    aka "flight number" in colloquial term
    """
    airline_designator: str
    flight_number: int
    
    def __post_init__(self):
        code = self.airline_designator
        self.airline_designator = code.upper()
        assert len(code) == 2
        assert 0 <= self.flight_number < 10_000

    def __iter__(self):
        yield self.airline_designator
        yield str(self.flight_number)
    
    def __str__(self):
        return ''.join(self)
    
    def format(self):
        return ' '.join(self)


if __name__ != '__main__':
    ...
    #globals().update()
    #Flight(status=Status.CANCLE)