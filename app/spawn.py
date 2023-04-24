from app.system import *
from app.utils import algorithm


functions = []

def wraper(func: Callable):
    from time import time
    
    def new(*arg, **kw):
        start = time()
        q = func(*arg, **kw)
        end = time()
        ms = (end - start) * 1000
        print(f'Generate {func.__qualname__} >> {round(ms, 2)} ms')
        return q
        
    functions.append(new)
    return new
          
            
@wraper
def airports():
    with open('data/airport.csv') as f:
        lines = csv.reader(f, delimiter=';')
        next(lines)
        for code, name, country, lat, lon in lines:
            Airline.airports.append(
                Airport(
                    name, code, country, (float(lat), float(lon))
                )
            )


@wraper
def aircrafts():
    with open('data/aircraft.json') as f:
        data: dict[str, list[list[dict[str, Any]]]]
        data = json.load(f)
        for model, desks in data.items():
            Airline.aircrafts.append(
                Aircraft(model, 
                    tuple(
                        Desk.generate(
                            (TravelClass(cabin['class']), cabin['configs']) 
                            for cabin in desk
                        ) for desk in desks
                    )
                )
            )


@wraper
def flights():
    numbers = iter(range(1, 10_000))
    Airline.flights.extend(
        chain(
            algorithm.P2P_flights(Airline.airports[:10], numbers, 1),
            algorithm.hub_flights(Airline.airports.get('bkk'), numbers, 2)
        )
    )


afares = []
@wraper
def fares():
    base_fare = (
        (
            [13_500, 7_500, 6_000], 
            [7_000, 7_500, 8_000, 9_000]
        ), (
            [33_000, 26_000, 23_000], 
            [20_000, 25_000, 28_000, 30_000]
        ), (
            [67_000, 78_000, 50_000], 
            [45_000, 46_000, 47_000, 53_000]
        )
    )
    func = lambda prices: [
        price * (1 + random()//2.5) for price in prices
    ]
    afares.extend(
        [
            (
                travel_class, Fare(
                    [*zip(PassengerType, func(pax))],
                    [*zip(SeatType, func(seat))]
                )
            ) for travel_class, (pax, seat) in zip(TravelClass, base_fare)
        ] for _ in range(7)
    )


@wraper
def flight_plans():
    for flight in Airline.flights:
        Airline.plans.append(
            FlightPlan(flight, 
                dt.date(2023, 12, 1), dt.date(2023, 12, 5), 
                default_aircraft=choice(Airline.aircrafts), 
                default_fares=choice(afares),
            )
        )


@wraper
def accounts():
    customers = [
        Customer(*attr) for attr in (
            ('Plum123', 'plum555', '65168516@kmitl.com', '0812345678'),
            ('user', '123456', 'user@uwu.com', '0000'),
            ('user1', '1234', 'user2@uwu.com', '0000'),
            ('user2', '123456789', 'user3@uwu.com', '0000'),
            ('use3', 'qweasd', 'user4@uwu.com', '0000'),
        )
    ]
    admins = [
        Admin(*attr) for attr in (
            ('admin', 'admin', 'jinny@uwu.com', '0000'),
        )
    ]
    for account in *admins, *customers:
        Airline.accounts.append(account)
        
        
@wraper
def search(
    origin: str = 'hkg', 
    destination: str = 'cai',
    date: dt.date = dt.date(2023, 12, 2)
):
    return Airline.search_journey(
        Airline.airports.get(origin), 
        Airline.airports.get(destination), 
        date,
    )