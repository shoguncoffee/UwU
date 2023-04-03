from .system import *

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
airport4 = Airport(
    'Don Mueang International Airport', 
    'DMK', 'Bangkok', 'Thailand'
)
airport5 = Airport(
    'Cairo International Airport', 
    'CAI', 'Cairo', 'Egypt'
)

aircraft1 = Aircraft(
    'Boeing 777', (
        Desk.generate(
            (TravelClass.BUSSINESS, [
                (4, [2, 2, 2])
            ]),
            (TravelClass.BUSSINESS, [
                (3, [2, 2, 2])
            ]),
            (TravelClass.ECONOMY, [
                (2, [3, 3, 3]),
                (8, [3, 4, 3]),
                (1, [0, 4, 0])
            ]),
            (TravelClass.ECONOMY, [
                (2, [3, 3, 3]),
                (8, [3, 4, 3]),
                (3, [3, 3, 3]),
                (1, [2, 3, 2]),
            ])
        ),
    )
)
aircraft2 = Aircraft(
    'Airbus 320', (
        Desk.generate(
            (TravelClass.BUSSINESS, [
                (4, [2, 2, 2])
            ]),
            (TravelClass.BUSSINESS, [
                (3, [2, 2, 2])
            ]),
            (TravelClass.ECONOMY, [
                (10, [3, 2, 3])
            ]),
            (TravelClass.ECONOMY, [
                (10, [3, 2, 3])
            ])
        ),
    )
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

client1 = Customer(
    'Plum123',
    '12345678',
    '516516@kmitl.com',   
    '0812345678',
)

if 0:
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
        Trip(search_outbound, TravelClass.ECONOMY),
        Trip(search_inbound, TravelClass.BUSSINESS)
    ]
    client1.request_booking(
        return_trip,
        contact1,
        passengerDetails1,
    )