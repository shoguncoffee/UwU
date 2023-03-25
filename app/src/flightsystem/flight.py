"""
take care of flight system
"""
from __future__ import annotations
from datetime import timedelta
from base import *

from src.constants import FlightStatus
if TYPE_CHECKING:
    from src import Aircraft, Airport, Seat, Booking, FlightReservation
    from main import Airline
    

class FlightCatalog:
    _instance: None | FlightCatalog = None
    
    def __new__(cls):    
        cls._instance = cls._instance or super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.__record: set[Flight] = set()
    
    @classmethod
    def add(cls, flight: Flight):
        cls 
    
    @classmethod
    def search(cls, designator: str):
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
        self.__designator = self.designator.upper()
        self.__reference = self.__reference or self.generate_reference()
    
    @property
    def designator(self) -> str:
        return self.__designator
    
    @property
    def duration(self) -> timedelta:
        crossday = timedelta(self.__arrival < self.__departure)
        d2 = datetime.combine(date.min + crossday, self.__arrival)
        d1 = datetime.combine(date.min, self.__departure)
        return d2 - d1
    
    @classmethod
    def generate_reference(cls):
        return ''
    
    
@dataclass
class FlightInstance:
    __flight: Flight #type: ignore
    __date: date #type: ignore
    __aircraft: Aircraft #type: ignore
    __base_price: float #type: ignore
    
    __booking_record: set[FlightReservation] = field(default_factory=set) #type: ignore
    __status: FlightStatus = FlightStatus.SCHEDULED #type: ignore
    
    @property
    def designator(self):
        return self.__flight.designator
    
    def update_status(self, status: FlightStatus):
        self.__status = status
    
    def get_reserved_seats(self):
        return set(
            seat.seat for reservation in self.__booking_record 
            for seat in reservation.seats
        )
        
@dataclass    
class FlightItinerary:
    __flights: list[FlightInstance] #type: ignore
        

@dataclass    
class Trip(FlightItinerary):
    __travel_class: TravelClass #type: ignore
    
