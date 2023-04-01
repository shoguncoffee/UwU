"""
system
"""
from __future__ import annotations
from .base import *
if TYPE_CHECKING:
    from app.src import *
from .catalog import *
from .booking_related import Booking

class Airline:
    name = 'Qatar Airways'
    designator = 'QR'
    
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, boot: bool = False):
        self.__schedule = ScheduleCatalog()
        self.__plan = FlightScheduling()
        self.__flight = FlightCatalog()
        self.__accounts = AccountCatalog()
        self.__aircraft = AircraftCatalog()
        self.__airport = AirportCatalog()
        
        if boot:
            self.init_aircraft()
            self.init_airport()
    
    @classmethod
    @property
    def schedule(cls):
        return cls._instance.__schedule
    
    @classmethod
    @property
    def flight(cls):
        return cls._instance.__flight
    
    @classmethod
    @property
    def accounts(cls):
        return cls._instance.__accounts
    
    @classmethod
    @property
    def aircraft(cls):
        return cls._instance.__aircraft
    
    @classmethod
    @property
    def airport(cls):
        return cls._instance.__airport
    
    @classmethod
    @property
    def plan(cls):
        return cls._instance.__plan
    
    def init_aircraft(self):
        with open('app/data/aircraft.csv') as f:
            data = ...
            return
    
    def init_airport(self):
        with open('app/data/airport.csv') as f:
            data = ...
            return
    
    @classmethod
    def create_booking(cls,
        creator: Customer,
        journey: list[Trip],
        contact: ContactInformation,
        *passengers: PassengerDetails,
    ):
        pax = len(passengers)
        if all(trip.bookable(pax) for trip in journey):
            booking = Booking(
                creator,
                journey,
                contact,
                passengers,
            )
            for reserved in booking.reservation:
                flight = reserved.flight
                if flight.bookable(reserved.travel_class, pax):
                    flight.booked(reserved)
                else: break
                
            else:
                creator.add_booking(booking)
                booking.pending()       
    
    @classmethod
    def register(cls, account: Account):
        if account.username not in cls.accounts:
            cls.accounts.append(account)
        else:
            return False


if __name__ == '__main__':
    Airline()
    print(Airline.aircraft)
    print(Airline.airport)