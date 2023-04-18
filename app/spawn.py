from .system import *
from datetime import date, time


# init system
Airline()


# init airports
airports = [
    Airport(*attr) for attr in (
        ('Homad International Airport', 
            'DOH', 'Doha', 'Qatar'),
        ('Suvarnabhumi International Airport',
            'BKK', 'Bangkok', 'Thailand'),
        ('London City Airport',
            'LCY', 'London', 'United Kingdom'),
        ('Don Mueang International Airport', 
            'DMK', 'Bangkok', 'Thailand'),
        ('Cairo International Airport', 
            'CAI', 'Cairo', 'Egypt'),
        ('Miami International Airport',
            'MIA', 'Miami','United States'),
        ('Taiwan Taoyuan International Airport',
            'TPE', 'Taipei', 'Taiwan'),
        ('Incheon International Airport',
            'ICN', 'Seoul', 'South Korea'),
        ('Hong Kong International Airport',
            'HKG', 'Hong Kong', 'Hong Kong'),
        ('Singapore Changi Airport',
            'SIN', 'Singapore', 'Singapore'),
        ('Sydney Kingsford Smith Airport',
            'SYD', 'Sydney', 'Australia'),
    )
]
for airport in airports:
    Airline.airports.append(airport)


# init aircrafts
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
    'Airbus A320', (
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
for aircraft in aircraft1, aircraft2:
    Airline.aircrafts.append(aircraft)


# init flights
flights = [
    Flight(*attr) for attr in (
        ('Q129', time(8, 0), time(15, 20), airports[0], airports[1]),
        ('Q265', time(17, 0), time(22, 30), airports[1], airports[2]),
        ('Q312', time(7, 0), time(12, 30), airports[2], airports[3]),
        ('Q413', time(16, 0), time(23, 20), airports[3], airports[4]),
        ('Q148', time(5, 15), time(8, 50), airports[4], airports[5]),
        ('Q254', time(11, 20), time(14, 40), airports[5], airports[6]),
        ('Q364', time(2, 15), time(5, 15), airports[6], airports[5]),
        ('Q3150', time(22, 35), time(1, 10), airports[5], airports[4]),
        ('Q404', time(0, 30), time(6, 0), airports[4], airports[3]),
        ('Q4413', time(17, 35), time(18, 20), airports[3], airports[2]),
        ('Q101', time(7, 25), time(9, 30), airports[2], airports[1]),
        ('Q236', time(23, 10), time(2, 50), airports[1], airports[0]),
        
        ('Q1648', time(10, 55), time(13, 40), airports[0], airports[2]),
        ('Q2103', time(9, 45), time(15, 55), airports[2], airports[3]),
        ('Q3491', time(4, 50), time(8, 40), airports[3], airports[1]),
        
        ('Q4167', time(11, 30), time(13, 20), airports[0], airports[4]),
        ('Q4169', time(14, 45), time(17, 15), airports[4], airports[1]),
    )
]
for flight in flights:
    Airline.flights.append(flight)


# init fares
fare0 = tuple(
    Fare(*attr) for attr in [(
            TravelClass.ECONOMY, [
                (PassengerType.ADULT, 13_500),
                (PassengerType.CHILD, 7_500),
                (PassengerType.INFANT, 6_000),
            ], [
                (SeatType.COMMON, 7_000),
                (SeatType.AISLE, 7_500),
                (SeatType.WINDOW, 8_000),
                (SeatType.LEGROOM, 9_000),
            ]
        ), (
            TravelClass.BUSSINESS, [
                (PassengerType.ADULT, 33_000),
                (PassengerType.CHILD, 26_000),
                (PassengerType.INFANT, 23_000),
            ], [
                (SeatType.COMMON, 20_000),
                (SeatType.AISLE, 25_000),
                (SeatType.WINDOW, 28_000),
                (SeatType.LEGROOM, 30_000),
            ]
        ),
    ]
)
fare1 = tuple(
    Fare(*attr) for attr in [(
            TravelClass.ECONOMY, [
                (PassengerType.ADULT, 15_000),
                (PassengerType.CHILD, 7_500),
                (PassengerType.INFANT, 6_000),
            ], [
                (SeatType.COMMON, 7_000),
                (SeatType.AISLE, 7_500),
                (SeatType.WINDOW, 8_000),
                (SeatType.LEGROOM, 9_000),
            ]
        ), (
            TravelClass.BUSSINESS, [
                (PassengerType.ADULT, 33_000),
                (PassengerType.CHILD, 26_000),
                (PassengerType.INFANT, 23_000),
            ], [
                (SeatType.COMMON, 20_000),
                (SeatType.AISLE, 25_000),
                (SeatType.WINDOW, 28_000),
                (SeatType.LEGROOM, 30_000),
            ]
        ),
    ]
)
fare2 = tuple(
    Fare(*attr) for attr in [(
            TravelClass.ECONOMY, [
                (PassengerType.ADULT, 20_000),
                (PassengerType.CHILD, 7_500),
                (PassengerType.INFANT, 6_000),
            ], [
                (SeatType.COMMON, 7_000),
                (SeatType.AISLE, 7_500),
                (SeatType.WINDOW, 8_000),
                (SeatType.LEGROOM, 9_000),
            ]
        ), (
            TravelClass.BUSSINESS, [
                (PassengerType.ADULT, 33_000),
                (PassengerType.CHILD, 26_000),
                (PassengerType.INFANT, 23_000),
            ], [
                (SeatType.COMMON, 20_000),
                (SeatType.AISLE, 25_000),
                (SeatType.WINDOW, 28_000),
                (SeatType.LEGROOM, 30_000),
            ]
        ),
    ]
)


# init flight plans
plans = [
    FlightPlan(flight, start, end, default_aircraft=aircraft, default_fares=fare) 
    for flight, start, end, aircraft, fare in (
        (flights[0], date(2023, 1, 1), date(2024, 1, 1), aircraft1, fare0),
        (flights[1], date(2023, 1, 1), date(2024, 1, 1), aircraft2, fare1),
        (flights[2], date(2023, 1, 1), date(2024, 1, 1), aircraft1, fare2),
        (flights[3], date(2023, 1, 1), date(2024, 1, 1), aircraft2, fare0),
        (flights[4], date(2023, 1, 1), date(2024, 1, 1), aircraft1, fare2),
        (flights[5], date(2023, 1, 1), date(2024, 1, 1), aircraft2, fare2),
        (flights[6], date(2023, 1, 1), date(2024, 1, 1), aircraft1, fare1),
        
        (flights[-5], date(2023, 4, 1), date(2023, 10, 1), aircraft2, fare0),
        (flights[-4], date(2023, 3, 1), date(2023, 10, 1), aircraft1, fare1),
        (flights[-3], date(2023, 2, 1), date(2023, 10, 1), aircraft2, fare1),
        (flights[-2], date(2023, 8, 1), date(2023, 10, 1), aircraft1, fare0),
        (flights[-1], date(2023, 9 ,1), date(2023, 11, 1), aircraft2, fare2),
    )
]
for plan in plans:
    Airline.plans.append(plan)


# init customers
customers = [
    Customer(*attr) for attr in (
        ('Plum123', 'plum555', '65168516@kmitl.com', '0812345678'),
        ('user', '123456', 'user@uwu.com', '0000'),
        ('user1', '1234', 'user2@uwu.com', '0000'),
        ('user2', '123456789', 'user3@uwu.com', '0000'),
        ('use3', 'qweasd', 'user4@uwu.com', '0000'),
    )
]
for customer in customers:
    Airline.accounts.append(customer)


# init admin
admins = [
    Admin(*attr) for attr in (
        ('admin', 'admin', 'jinny@uwu.com', '0000'),
    )
]
for admin in admins:
    Airline.accounts.append(admin)


# test
plum = Airline.accounts.get('Plum123')
assert isinstance(plum, Customer)

qatar = Airline.airports.get('DOH')
thailand = Airline.airports.get('BKK')

passengerDetails1 = PassengerDetails(
    'Plum', 'Arpleum',
    date(1999, 1, 1),
    'Thai', '254123543',
    GenderType.MALE,
    PassengerType.ADULT,
)
contact1 = ContactInformation(
    passengerDetails1,
    '0812345678', '516516@kmitl.com'
)
results = Airline.search_journey(
    qatar, thailand,
    dt.date(2023, 9, 10)
)
Airline.create_booking(plum, [
        (results[0], TravelClass.ECONOMY),
    ], contact1, passengerDetails1,
)

booking = plum.bookings[0]
reservation = booking.reservations[0]
instance = reservation.flight

seats = instance.aircraft.all_seats
seatiter = iter(seats)
seat1 = next(seatiter)
seat2 = next(seatiter)

Airline.select_seats(
    reservation, [
        (passengerDetails1, seat1)
    ]
)


#Testing Start Here
client1 = plum

#View Booking Use Case
Airline.create_booking(plum, [
        (results[0], TravelClass.ECONOMY),
    ], contact1, passengerDetails1,
)
# booking1 = Booking(client1, return_trip, contact1, (passengerDetails1,))
# client1.add_booking(booking1)

def test_viewbooking(): #Manually Create adn Add a Booking
    my_list = client1.view_booking(client1.get_booking(booking.id))

#booking = client1.select_booking(1)
#booking2 = client1.select_booking(2)

#print(my_list)

#Testing Modify Booking
#Airline.modify_booking(client1, 1)

from fastapi import FastAPI

app = FastAPI()

@app.get("/booking_info", tags=['booking'])
async def view_booking(booking_no: UUID) -> dict:
    book = client1.get_booking(booking_no)
    return {"my_list" : client1.view_booking(book)}

@app.put("/booking_info", tags=['booking'])
async def update_booking() -> dict:
    ...