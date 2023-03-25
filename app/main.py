"""
"""
from __future__ import annotations
from .base import *
from .src import *
from fastapi import FastAPI

if TYPE_CHECKING:
    from src import (
        Customer, 
        ContactInformation, 
        PassengerDetails, 
        FlightInstance, 
        SeatReservation, 
        Booking,
        Trip,
        TravelClass
    )

class Airline:
    name = 'Qatar Airways'
    designator = 'QR'

    @classmethod 
    def create_booking(cls,
            creator: Customer,
            journey: list[Trip],
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
        
    @classmethod 
    def asd(cls):
        ...
        
        
if __name__ == '__main__':
    '''
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
    '''