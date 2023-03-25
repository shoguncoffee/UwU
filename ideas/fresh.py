from __future__ import annotations
from typing import Optional
from enum import Enum
from datetime import time, datetime, date
from dataclasses import dataclass

FlightStatus = Enum(
    'FlightStatus', 'SCHEDULED CANCELLED DELAYED'
)
PassengerType = Enum(
    'PassengerType', 'ADULT CHILD INFANT'
)
TravelClass = Enum(
    'TravelClass', 'Economy Bussiness First'
)
AccountStatus = Enum(
    'AccountStatus', 'PENDING ACTIVE SUSPENDED'
)
BookingStatus = Enum(
    'BookingStatus', 'PENDING CONFIRMED CANCELLED'
)
SeatType = Enum(
    'SeatType', 'STANDARD'
)
GenderType = Enum(
    'GenderType', 'MALE FEMALE'
)

class Airline:
    def __init__(self):
        self.name = 'Qatar Airways'
    
    @classmethod 
    def create_booking(cls,
            creator: Customer,
            journey: list[tuple[FlightInstance, TravelClass]],
            passengers: list[PassengerDetails],
            contact: ContactInformation
        ):
        reserve = []
        for passenger in passengers:
            reseved = SeatReservation(passenger,None)
            reserve.append(reseved)
        
        reference = '15464646'
        
        print('create booking')
        return Booking(
            creator,
            reference,
            passengers,
            reserve,
            contact,
        )
            

class Airport:
    def __init__(self, 
            name: str, 
            location_code: str,
            city: str,
            country: str
        ):
        self.__name = name
        self.__location_code = location_code
        self.__city = city
        self.__contry = country
       
        
class Aircraft:
    def __init__(self, 
            name: str, 
            type: str,
            cabin: list[CabinLayout],
        ):
        self.__name = name
        self.__type = type
        self.__cabin = cabin 
    
    def get_all_seat(self):
        ...
    
    
class CabinLayout:
    def __init__(self, 
            desk: int, 
            cls: TravelClass,
            seats: list[Seat],
        ):
        self.__desk = desk
        self.__class_type = cls
        self.__seats = seats
    
    
class Seat:
    def __init__(self,
            row: int,
            column: int,
            type: SeatType,
            description: str
        ):
        self.__row = row
        self.__column = column
        self.__type = type
        self.__description = description
        

class SeatPrice:
    def __init__(self,
            price: float,
            type: SeatType
        ):
        self.__price = price
        self.__type = type
        

class Flight:
    def __init__(self, 
            designator: str,
            departure: time, 
            arrival: time, 
            origin: Airport, 
            destination: Airport, 
            reference: Optional[str] = None,
    ):
        self.__designator = designator
        self.__departure = departure
        self.__arrival = arrival
        self.__origin = origin
        self.__destination = destination
        self.__reference = reference or self.generate_reference()

    def generate_reference(self):
        return
    

class FlightInstance:
    def __init__(self, 
            flight: Flight,
            date: date, 
            aircraft: Aircraft, 
            base_price: float
        ):
        self.__flight = flight
        self.__date = date
        self.__aircraft = aircraft
        self.__base_price = base_price
        
        self.__booking_records = []
        self.__status = FlightStatus.SCHEDULED
        
    def get_designator(self):
        pass
    
    def get_reserved_seats(self):
        pass
        
    def modify_flight_instance(self, flight, date, aircraft):
        pass
    
        
class PassengerDetails:
    def __init__(self,  
            forename: str, 
            surname: str, 
            birthdate: date, 
            gender: GenderType, 
            passport_id: str, 
            type: PassengerType,
            nationality: str, 
            travel_document: Optional[str] = None
        ):
        self.__forename = forename
        self.__surname = surname
        self.__birthdate = birthdate
        self.__gender = gender
        self.__passport_id = passport_id
        self.__type = type
        self.__nationality = nationality
        self.__travel_document = travel_document
        
    
class SeatReservation:
    def __init__(self,
            passenger: PassengerDetails,
            seat: Seat | None
        ):
        self.__passenger = passenger
        self.__seat = seat


class Booking:
    def __init__(self,
            creator: Customer,
            reference: str, 
            passenger: list[PassengerDetails],
            reservation: list[FlightReservation],
            contactinfo: ContactInformation,
        ):
        self.__creator = creator
        self.__reference = reference or self.generate_reference()
        self.__reservation = reservation
        self.__contactinfo = contactinfo
        self.__passenger = passenger
        
        self.__status = BookingStatus.PENDING
        
        self.__date = datetime.now().date()

    def generate_reference(self):
        pass
    
    def select_seat(self):
        pass


class FlightReservation:
    def __init__(self,
            cls: TravelClass,
            holder: Booking, 
            flight: Flight,
            seats: list[Seat], 
        ):
        self.__class_of_service = cls
        self.__holder = holder
        self.__flight = flight
        self.__seats = seats


class ContactInformation:
    def __init__(self,
        name: str,
        phone_country: str,
        phone: str,
        email: str
    ):
        self.__name = name
        self.__phone = phone
        self.__phone_country = phone_country
        self.__email = email


class Account:
    def __init__(self,
            username: str,
            email: str,
            password: str,
        ):
        self.__username = username
        self.__email = email
        self.__password = password
        self.__status = AccountStatus.ACTIVE


class Customer(Account):
    def __init__(self,
            phone: str,
            **kwarg
        ):
        super().__init__(**kwarg)
        self.__phone = phone
        self.__booking = []
    
    def request_create_booking(self,
            journey: list[tuple[FlightInstance, TravelClass]],
            passenger: list[PassengerDetails],
            contact: ContactInformation
        ):
        booking = Airline.create_booking(
            self, 
            journey, 
            passenger, 
            contact
        )
        self.__booking.append(booking)
        
        

if __name__ == '__main__':
    airline = Airline()
    airport1 = Airport(
        'Homad International Airport',
        'Doh',
        'Doha',
        'Qatar',
    )
    airport2 = Airport(
        'Suvarnabhumi International Airport',
        'BKK',
        'Bangkok',
        'Thailand',
    )
    airport3 = Airport(
        'London City Airport',
        'LCY',
        'London',
        'United Kingdom'
    )
    cabin1 = CabinLayout(
        1,
        TravelClass.Economy,
        [
            Seat(1, 1, SeatType.STANDARD, 'Driver'),
            Seat(1, 2, SeatType.STANDARD, 'Driver2'),
            Seat(1, 3, SeatType.STANDARD, 'Driver3'),
        ]
    )
    aircraft1 = Aircraft(
        'Boeing 747',
        'A',
        [cabin1] 
    )
    flight1 = Flight(
        'Q0001',
        time(hour=8, minute=0),
        time(hour=15, minute=20),
        airport1,
        airport2,
    )
    flight2 = Flight(
        'Q0002',
        time(hour=17, minute=0),
        time(hour=22, minute=30),
        airport2,
        airport3
    )
    flight3 = Flight(
        'Q0003',
        time(hour=7, minute=0),
        time(hour=12, minute=30),
        airport3,
        airport2,
    )
    flight4 = Flight(
        'Q0004',
        time(hour=16, minute=0),
        time(hour=23, minute=20),
        airport2,
        airport1
    )
    flightin1 = FlightInstance(
        flight1,
        date(day=18, month=1, year=2023),
        aircraft1,
        50_000
    )
    flightin2 = FlightInstance(
        flight2,
        date(day=18, month=1, year=2023),
        aircraft1,
        50_000
    )
    flightin3 = FlightInstance(
        flight3,
        date(day=23, month=1, year=2023),
        aircraft1,
        50_000
    )
    flightin4 = FlightInstance(
        flight4,
        date(day=23, month=1, year=2023),
        aircraft1,
        50_000
    )
    
    client1 = Customer(
         phone = '0812345678',
         username = 'Plum123',
         password = '12345678',
         email = '516516@kmitl.com',   
    )
    contact1 = ContactInformation(
        'Arpleum',
        '+66',
        '0812345678',
        '516516@kmitl.com'
    )
    passengerDetails1 = PassengerDetails(
        'Plum',
        'Arpleum',
        date(year=1999, month=1, day=1),
        GenderType.MALE,
        '254123543',
        PassengerType.ADULT,
        'Thai',
        None
    )
    client1.request_create_booking(
        [
            (flightin1, TravelClass.Economy), 
            (flightin2, TravelClass.Economy), 
            (flightin3, TravelClass.Economy), 
            (flightin4, TravelClass.Economy)
        ],
        [passengerDetails1],
        contact1
    )
