"""
system
"""
from __future__ import annotations
from .base import *
if TYPE_CHECKING:
    from app.src import *
from .booking_related import Booking

class Airline(Singleton):
    _instance: Airline
    name = 'Qatar Airways'
    designator = 'QR'
    
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
        all_reservation = [
            FlightReservation(flight, trip.travel_class) for trip in journey for flight in trip.flights
        ]
        booking = Booking(
            creator,
            all_reservation,
            passengers,
            contact
        )
        creator.add_booking(booking)
        
    @classmethod 
    def asd(cls):
        cls._instance
