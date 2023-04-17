"""
system
"""
from __future__ import annotations
from .base import *

from .src import *


class Airline:
    name = 'Qatar Airways'
    designator = 'QR'
    
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.__aircrafts = AircraftCatalog()
        self.__airports = AirportCatalog()
        self.__accounts = AccountCatalog()
        self.__flights = FlightCatalog()
        self.__schedules = ScheduleCatalog()
        self.__plans = FlightScheduling()
    
    @classmethod
    @property
    def schedules(cls):
        return cls._instance.__schedules
    
    @classmethod
    @property
    def flights(cls):
        return cls._instance.__flights
    
    @classmethod
    @property
    def accounts(cls):
        return cls._instance.__accounts
    
    @classmethod
    @property
    def aircrafts(cls):
        return cls._instance.__aircrafts
    
    @classmethod
    @property
    def airports(cls):
        return cls._instance.__airports
    
    @classmethod
    @property
    def plans(cls):
        return cls._instance.__plans
    
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
        result = cls.schedules[date].route_search(
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
        daylimit: int = 2,
    ): 
        possible = [
            cls.search_segment(
                org, dst, date, pax
            ) for org, dst in zip(stops, stops[1:])
        ]
        for result in product(*possible):
            ...
            
        results = ...
        return
    
    @classmethod
    def search_return(cls, 
        origin: Airport, 
        destination: Airport, 
        dates: tuple[date, date],
        pax: int,
    ):  
        return search_multicity(
            
        )
        ...
        
    @classmethod
    def search_multicity(cls, 
        origin: Airport, 
        destinations: tuple[date, Airport], 
        pax: int,
    ):  
        return [
            cls.search_journey([origin, destination], date, pax)
            for date in dates
        ]
        ...

    #Booking Features Branch Begins Here
    @classmethod
    def modify_booking(cls, customer: Customer, booking_no):
        booking = customer.select_booking(booking_no)
        passenger = booking.passenger
        contact = booking.contactinfo
        
        for i in passenger:
            pass
        
    #What you going to do now is that customer(Frontend) will request modify through Airline, passing current Customer Account