from app.base import *
from app.src import *
from string import ascii_uppercase


class SearchHelper:
    def __init__(self,
        start: Airport,
        target: Airport,
        date: dt.date,
        pool: Collection[FlightInstance],
        multiplier: float = 1.5,
        limit_transit: dt.timedelta = dt.timedelta(hours=24),
    ):
        self.pool = pool
        self.target = target
        self.limit_transit = limit_transit
        self.limit_duration = approx_time(start, target) * multiplier
        
        condition = lambda i: i.flight.origin is start and i.date == date
        self.leadings = filter(condition, pool)

    def result(self): 
        for first in self.leadings:
            if first.flight.destination is self.target:
                yield FlightItinerary([first])
                
            else:
                for itinerary in self.conjugate(first):
                    yield FlightItinerary(itinerary)

    def conjugate(self, *path: FlightInstance):
        """
        find all possible sequence of FlightInstance 
        that can take from origin to destination in limit duration
            - path: `tuple[FlightInstance, ...]`
                - len(path) > 1
        """
        path_itinerary = FlightItinerary(path)
        limit_flight_time = self.limit_duration - path_itinerary.flight_time()
        prev = path[-1]
        footwork = [footprint.flight.origin for footprint in path]
        
        for instance in self.pool:
            this = instance.flight
            if (
                this.origin is prev.flight.destination
                and this.destination not in footwork
                and self.limit_transit > prev.transit_time(instance) > dt.timedelta(minutes=30)
                and limit_flight_time > instance.duration
            ):
                if this.destination is self.target:
                    yield *path, instance

                else:
                    yield from self.conjugate(*path, instance)


def approx_time(
    airport1: Airport, 
    airport2: Airport,
    speed: float = 700,
    common: dt.timedelta = dt.timedelta(minutes=5)
):
    """
    approximate flight time between two airports
        - speed: `float`
            - average speed in km/h
    """
    distance = airport1.distance(airport2).km
    time = dt.timedelta(hours=distance/speed)
    quotient = time.seconds // common.seconds + 1
    
    return common * (quotient + randrange(5))


def generate_flight(
    designator: str,
    origin: Airport,
    destination: Airport,
    duration: Optional[dt.timedelta] = None,
):
    """
        randomize flight departure time and calculate arrival time
    """
    time = dt.timedelta(
        hours=randrange(24), 
        minutes=randrange(0, 60, 5)
    )
    departure = dt.datetime.min + time
    duration = duration or approx_time(origin, destination)
    arrival = departure + duration

    flight = Flight(
        designator,
        departure.time(), arrival.time(),
        origin, destination,
    )
    return flight


def P2P_flights(
    airports: Iterable[Airport], 
    designators: Iterator[str],
    times: int = 1,
):
    """
    ### Point-to-point
        - https://en.wikipedia.org/wiki/Point-to-point_transit
    """
    for origin, destination in combinations(airports, 2):
        duration = approx_time(origin, destination)
        if duration > dt.timedelta(minutes=30):
            for _ in range(times):
                yield generate_flight(next(designators), origin, destination, duration)
                yield generate_flight(next(designators), destination, origin, duration)
            

def hub_flights(
    airports: Iterable[Airport],
    hub: Airport, 
    designators: Iterator[str],
    times: int = 1,
):
    """
    ### Spoke-Hub
        - https://en.wikipedia.org/wiki/Airline_hub
        - https://en.wikipedia.org/wiki/Spoke%E2%80%93hub_distribution_paradigm  
    """
    for destination in airports:
        duration = approx_time(hub, destination)
        if destination is not hub and duration > dt.timedelta(minutes=30):
            for _ in range(times):
                yield generate_flight(next(designators), hub, destination, duration)
                yield generate_flight(next(designators), destination, hub, duration)


def generate_cabin(
    travel_class: TravelClass,
    initial_row: int,
    layouts: Sequence[Sequence[int]],
):
    """
    generate a `Cabin`, for using in spawn.py
    """
    seats: list[Seat] = []
    relative_row = 0
    
    for lenght, *config in layouts:
        width = sum(config)
        gaps = len(config) - 1
        aisle_columns = {
            sum(config[:column+1]) - i
            for column, i in product(range(gaps), range(2)) 
        }
        for row, column in product(range(lenght), range(width)):
            conditions = {
                SeatType.AISLE: column in aisle_columns,
                SeatType.WINDOW: column in (0, width-1),
                SeatType.LEGROOM: relative_row + row == 0,
            }
            type = reduce(
                operator.or_, 
                compress(conditions, conditions.values()), 
                SeatType(0)
            )
            absolute_row = initial_row + relative_row + row
            seat_number = f'{ascii_uppercase[column]}{1 + absolute_row}'
            
            seat = Seat(absolute_row, column, seat_number, type)
            seats.append(seat)
            
        relative_row += lenght
        
    return Cabin(travel_class, seats)


def generate_deck(
    cabin_layout: Iterable[tuple[
        TravelClass, Sequence[Sequence[int]]
    ]]
):
    """
    generate a `Deck`, for use in spawn.py
    """
    cabins = []
    row = 0
    for travel_class, layout in cabin_layout:
        cabin = generate_cabin(travel_class, row, layout)
        
        cabins.append(cabin)
        row += sum(lenght for lenght, *_ in layout) 

    return Deck(cabins)