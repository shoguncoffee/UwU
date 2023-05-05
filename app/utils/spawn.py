from app.base import *
from app.src import *

from app.airline import Airline
from . import algorithm
from time import time


def timmer(func: Callable):
    def new(*arg, **kw):
        start = time()
        return_value = func(*arg, **kw)
        ms = (time() - start) * 1000
        print(f'Generate {func.__qualname__} >> {round(ms, 2)} ms')
        
        return return_value
    return new


def add_airports(system: Airline):
    with open('data/airport.csv') as f:
        lines = csv.reader(f, delimiter=';')

        # skip header line of csv file
        next(lines)
        
        for code, name, country, lat, lon in lines:
            airport = Airport(name, code, country, (float(lat), float(lon)))
            
            system.airports.add(airport)


@timmer
def add_aircrafts(system: Airline):
    with open('data/aircraft.json') as f:
        data: dict[str, list[list[dict[str, Any]]]]
        data = json.load(f)
        
        for model, decks_data in data.items():
            decks = [
                algorithm.generate_deck(
                    (TravelClass(cabin['class']), cabin['configs']) 
                    for cabin in deck
                ) for deck in decks_data
            ]
            
            aircraft = Aircraft(model, decks)
            system.aircrafts.add(aircraft)


@timmer
def add_flights(system: Airline):
    airline_designator = system.designator
    airports = system.airports.items
    choiced_airports = system.airports.items[:15]
    bkk = system.airports.get('bkk')
    
    # for assign flight number
    numbers = (f'{airline_designator}{n}' for n in range(1, 10_000))

    system.flights.extend(
        chain(
            algorithm.P2P_flights(choiced_airports, numbers, 1),
            algorithm.hub_flights(airports, bkk, numbers, 2)
        )
    )


@timmer
def add_flight_plans(system: Airline):
    base_fare = {
        TravelClass.ECONOMY: (
            [13_500, 7_500, 6_000], # passenger price
            [7_000, 7_500, 8_000, 9_000] # seat price
        ), 
        TravelClass.BUSSINESS: (
            [33_000, 26_000, 21_000], 
            [20_000, 25_000, 28_000, 30_000]
        ), 
        TravelClass.FIRST: (
            [68_000, 57_000, 48_000], 
            [35_000, 36_000, 37_000, 33_000]
        )
    }
    distort = lambda prices: [
        200 * round(price/200 * (1 + random()/2)) for price in prices
    ]
    fares: list[list[tuple[TravelClass, Fare]]] = []
    
    for _ in range(10):
        price: list[tuple[TravelClass, Fare]] = []

        for travel_class, (passenger_price, seat_price) in base_fare.items():
            passenger_fare = [
                *zip(PassengerType, distort(passenger_price))
            ]
            seat_fare = [
                *zip(SeatType, distort(seat_price))
            ]
            
            fare = Fare(passenger_fare, seat_fare)
            price.append(
                (travel_class, fare)
            )
            
        fares.append(price)


    for flight in system.flights:
        random_aircraft = choice(system.aircrafts.items)
        random_fare = choice(fares)
        
        plan = FlightPlan(flight, 
            dt.date(2023, 6, 1), 
            dt.date(2023, 6, 10), 
            default_aircraft=random_aircraft, 
            default_fares=random_fare,
        )
        system.plans.add(plan)

    system.update_flight()


def add_accounts(system: Airline):
    customers = [
        Customer('Plum123', 'plum555', '65168516@kmitl.com', '0812345678'),
        Customer('user1', '123498765', 'user1@uwu.com', '0821024675'),
        Customer('user2', '123456789', 'user2@uwu.com', '0612345678'),
    ]
    for account in customers:        
        system.accounts.add(account)
        
        
@timmer
def search(system: Airline,
    origin: str, 
    destination: str,
    date: dt.date = dt.date(2023, 6, 1)
):
    """
        test search journey
    """
    ori_airport = system.airports.get(origin)
    dst_airport = system.airports.get(destination)
    
    return system.search_journey(ori_airport, dst_airport, date)


def print_results(results: list[FlightItinerary]):
    for itinerary in results:
        print('-', end=' ')
        
        for instance in itinerary:
            flight = instance.flight
            print(
                f'{flight.designator: <6} {instance.date} |',
                f'{flight.origin.code} {flight.departure: %H:%M} -> {flight.destination.code} {flight.arrival: %H:%M}',
                end = ' '*3
            )
        print()