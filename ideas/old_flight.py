r'''
from __future__ import annotations
from base import *

from src.constants import FlightStatus
from src import Aircraft
from src import Airport
from src import seat

class FlightGenerator:
    """
    a base policy for generating flight
    """
    def __init__(self, airline_designator: str = 'UW'):
        ...

    def generate_flight(self):
        ...
    
    def generate_designator(self):
        ...


@dataclass
class FlightManager:
    """
    manipulate a flight
    """
    __flight: set[Flight]
    __flight_generater: FlightGenerator = FlightGenerator()
    
    def create_flight(self, origin: Airport, destination: Airport):
        self.__flight_generater.generate_flight()
        

@dataclass
class FlightService:
    """
    represent and organize a flight service
    """
    __reservation: set[seat.Seat]
    __status: Status = Status.SCHEDULED
    
    def __post_init__(self):
        ...
        
    @property
    def passenger(self):
        return len(self.reservation)
    
    def is_full(self, seat_class: Optional[seat.Class] = None):
        if seat_class is None:
            return self.passenger == self.aircraft.capacity
        else:
            ...
            
            return self.passenger == self.aircraft.capacity


@dataclass
class Flight:
    """
    contain information about a flight
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
'''