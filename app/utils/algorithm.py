from app.system import *


class SearchHelper:
    def __init__(self,
        start: Airport,
        target: Airport,
        date: dt.date,
        pool: Collection[FlightInstance],
        multiplier: float = 2,
        limit_transit: dt.timedelta = dt.timedelta(hours=24),
    ):
        self.pool = pool
        self.target = target
        self.limit_transit = limit_transit
        self.limit_duration = approx_time(start, target) * multiplier
        
        condition = lambda i: i.flight.origin is start and i.date == date
        self.leadings = filter(condition, pool)

    def __iter__(self):
        return self.yielder()

    def yielder(self): 
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
            - limit: `datetime.timedelta`
                - maximum flight time of the path
        """
        limit_flight_time = self.limit_duration - FlightItinerary.flight_time(path)
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
    ...
        - speed: `float`
            - average speed in km/h
    """
    distance = airport1.distance(airport2).km
    time = dt.timedelta(hours=distance/speed)
    quotient = time.seconds // common.seconds + 1
    
    return common * (quotient + randrange(5))


def generate_flight(
    number: int,
    origin: Airport,
    destination: Airport,
):
    """
        randomize flight time
    """
    time = dt.timedelta(
        hours=randrange(24), 
        minutes=randrange(0, 60, 5)
    )
    departure = dt.datetime.min + time
    arrival = departure + approx_time(origin, destination)
    
    return Flight(
        f'{Airline.designator}{number}',
        departure.time(), arrival.time(),
        origin, destination,
    )


def P2P_flights(
    airports: Iterable[Airport], 
    numbers: Iterator[int],
    times: int = 1,
):
    """
    ### Point-to-point
    
        https://en.wikipedia.org/wiki/Point-to-point_transit
    """
    for route in combinations(airports, 2):
        for _ in range(times):
            yield generate_flight(next(numbers), *route)
            yield generate_flight(next(numbers), *reversed(route))
            

def hub_flights(
    hub: Airport, 
    numbers: Iterator[int],
    times: int = 1,
):
    """
    ### Spoke-Hub
    
        https://en.wikipedia.org/wiki/Airline_hub
        https://en.wikipedia.org/wiki/Spoke%E2%80%93hub_distribution_paradigm  
    """
    for destination in Airline.airports:
        if destination is not hub:
            for _ in range(times):
                yield generate_flight(next(numbers), hub, destination)
                yield generate_flight(next(numbers), destination, hub)