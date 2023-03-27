"""
system
"""
from __future__ import annotations
from .base import *

if TYPE_CHECKING:
    from src import *
"""
class Airline(Singleton):
    name = 'Qatar Airways'
    designator = 'QR'
    _instance: Airline
    
    def __init__(self):
        self.__accounts: set[Account] = set()
        
        self.init_aircraft()
        self.init_airport()
    
    def init_aircraft(self):
        return
        with open('app/data/aircraft.json') as f:
            data = ...
    
    def init_airport(self):
        return
        with open('app/data/airport.json') as f:
            data = ...
            
    def load(self):
        self._instance
    
    @classmethod
    def create_booking(cls,
        creator: Customer,
        journey: list[Trip],
        passengers: list[PassengerDetails],
        contact: ContactInformation
    ):
        reserve = [
            SeatReservation(passenger, None) for passenger in passengers
        ]
        for trip in journey:
            for flight in trip.flight:
                
                FlightReservation(
                    trip.travel_class,
                    ,
                    flight,
                    reserve
                )
        
        return Booking(
            creator,
            passengers,
            ,
            contact,
        )
        
    @classmethod 
    def asd(cls):
        cls._instance
        
"""