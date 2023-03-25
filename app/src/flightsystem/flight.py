"""
take care of flight system
"""
from __future__ import annotations
from base import *

from src.constants import FlightStatus
if TYPE_CHECKING:
    from src import Aircraft, Airport, Seat, Booking
    from main import Airline
    
@dataclass
class FlightCatalog:
    __record: set[Flight] #type: ignore
    
    def add(self):
        ...
    
    
@dataclass
class Flight:
    __designator: str #type: ignore
    __departure: time #type: ignore
    __arrival: time #type: ignore
    __origin: Airport #type: ignore
    __destination: Airport #type: ignore
    __reference: Optional[str] = None #type: ignore
    
    def __post_init__(self):
        self.__reference = self.__reference or self.generate_reference()
    
    @property
    def designator(self):
        return self.__designator
    
    @property
    def duration(self):  
        return self.__arrival - self.__departure
    
    @classmethod
    def generate_reference(cls):
        return ''
    
    
@dataclass
class FlightInstance:
    __flight: Flight #type: ignore
    __date: date #type: ignore
    __aircraft: Aircraft #type: ignore
    __base_price: float #type: ignore
    
    __booking_records: set[Booking] = field(default_factory=set) #type: ignore
    __status: FlightStatus = FlightStatus.SCHEDULED #type: ignore
        
    def get_designator(self):
        pass
    
    def get_reserved_seats(self):
        pass
        
    def modify_flight_instance(self, flight, date, aircraft):
        pass