r"""
command-line interface of this package (UwU/app)

for this package:
- `\UwU> python -m app`


for individual submodule in this package:
- ``\UwU> python -m app.<module>`
"""
import pickle
from .src import *
from base import *
from .system import Airline

Airline()

airport1 = Airport(
    'Homad International Airport',
    'Doh', 'Doha', 'Qatar'
)
airport2 = Airport(
    'Suvarnabhumi International Airport',
    'BKK', 'Bangkok', 'Thailand'
)
airport3 = Airport(
    'London City Airport',
    'LCY', 'London', 'United Kingdom'
)

aircraft1 = Aircraft(
    'Boeing 747',
    (
        Desk((
            CabinLayout(
                TravelClass.Economy, frozenset([
                    Seat(1, 1, SeatType.STANDARD),
                    Seat(1, 2, SeatType.STANDARD),
                    Seat(1, 3, SeatType.STANDARD),
                ])
            ),
            CabinLayout(
                TravelClass.Bussiness, frozenset([
                    Seat(1, 1, SeatType.STANDARD),
                    Seat(1, 2, SeatType.STANDARD),
                    Seat(1, 3, SeatType.STANDARD),
                ])
            )
        ))
    ,)
)

flight1 = Flight(
    'Q0001',
    time(8, 0), time(15, 20),
    airport1, airport2,
)
flight2 = Flight(
    'Q0002',
    time(17, 0), time(22, 30),
    airport2, airport3
)
flight3 = Flight(
    'Q0003',
    time(7, 0), time(12, 30),
    airport3, airport2,
)
flight4 = Flight(
    'Q0004',
    time(16, 0), time(23, 20),
    airport2, airport1
)

flightin1 = FlightInstance(
    date(2023, 1, 18), flight1, 
    aircraft1, 50_000
)
flightin2 = FlightInstance(
    date(2023, 1, 18), flight2, 
    aircraft1, 50_000
)
flightin3 = FlightInstance(
    date(2023, 1, 23), flight3, 
    aircraft1, 50_000
)
flightin4 = FlightInstance(
    date(2023, 1, 23), flight4, 
    aircraft1, 50_000
)

client1 = Customer(
    'Plum123',
    '12345678',
    '516516@kmitl.com',   
    '0812345678',
)
passengerDetails1 = PassengerDetails(
    'Plum', 'Arpleum',
    date(1999, 1, 1),
    'Thai', '254123543',
    GenderType.MALE,
    PassengerType.ADULT,
)
contact1 = ContactInformation(
    passengerDetails1,
    '+66', '0812345678',
    '516516@kmitl.com'
)
search_outbound = FlightItinerary(flightin1, flightin2)
search_inbound = FlightItinerary(flightin3, flightin4)

return_trip = [
    Trip(search_outbound, TravelClass.Economy),
    Trip(search_inbound, TravelClass.Bussiness)
]
client1.request_booking(
    return_trip,
    contact1,
    passengerDetails1,
)

if __name__ == '__main__a':
    with open('', 'rb') as f:
        pickle.load(f)
    if 0:
        Airline()