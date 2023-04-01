"""
system
"""
from __future__ import annotations
from .base import *

if TYPE_CHECKING:
    from app.src import *
    
from .src.catalog import *
from .src.booking_related import Booking


class Airline:
    name = 'Qatar Airways'
    designator = 'QR'
    
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.__aircraft = AircraftCatalog()
        self.__airport = AirportCatalog()
        self.__schedule = ScheduleCatalog()
        self.__plan = FlightScheduling()
        self.__flight = FlightCatalog()
        self.__accounts = AccountCatalog()
    
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
        if account not in cls.accounts:
            cls.accounts.add(account)
            return True
        
        return False

    @classmethod
    def search_segment(cls,
        origin: Airport, 
        destination: Airport, 
        date: date,
        pax: int,
    ):
        result = cls.schedule[date].search(
            origin, destination, 
        )
        return [
            flight for flight in result
            if flight.bookingable(pax)
        ]
    
    @classmethod
    def search_journey(cls,
        stops: list[Airport], 
        date: date,
        pax: int,
    ): 
        for org, dst in zip(stops, stops[1:]):
            result = cls.search_segment(
                org, dst, date, pax
            )
    
    @classmethod
    def search_return(cls, 
        origin: Airport, 
        destination: Airport, 
        dates: tuple[date, date],
        pax: int,
    ):  
        return [
            cls.search_segment(origin, destination, date, pax)
            for date in dates
        ]
    

if __name__ == '__main__':
    print(Airline.aircraft)
    print(Airline.airport)