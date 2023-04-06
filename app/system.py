"""
system
"""
from __future__ import annotations
from .base import *
from .src import *


class Airline:
    """
    represent the system of this project
    """
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
            cls.accounts.append(account)
            return True
        
        return False
    
    @classmethod
    def search_journey(cls,
        origin: Airport, 
        destination: Airport, 
        date: date,
        pax: int = 0,
        duration_cutoff: timedelta = timedelta(hours=17),
    ): 
        """
        return a list of FlightItinerary by any possible FlightInstance
        that can take from origin to destination in limit duration
        """
        possible_instance: list[FlightInstance] = []
        for _date in daterange(duration_cutoff.days, date):
            schedule = Airline.schedules.search(_date)
            possible_instance.extend(schedule or [])
        
        possible_itinerary = _path_algorithm(
            start = origin,
            target = destination,
            depature = date,
            pool = possible_instance,
            limit = duration_cutoff
        )
        result = [
            itinerary for itinerary in possible_itinerary 
            if itinerary.bookable(pax)
        ]
        result.sort(
            key = lambda itinerary: itinerary.minimal_fare()
        )
        return result
    
    @classmethod
    def search_return(cls, 
        origin: Airport, 
        destination: Airport, 
        dates: tuple[date, date],
        pax: int,
    ): 
        outbound = cls.search_journey(
            origin, destination, dates[0], pax
        )
        inbound = cls.search_journey(
            destination, origin, dates[1], pax
        )
        return outbound, inbound
        
        
def _path_algorithm(
    *path: FlightInstance, 
    start: Airport,
    target: Airport,
    pool: Sequence[FlightInstance],
    limit: timedelta,
    depature: Optional[date] = None,
) -> Generator[FlightItinerary, None, None]:
    
    cumulative_time = sum(
        [inst.flight.duration for inst in path], 
        start = timedelta()
    )
    for instance in pool:
        if instance not in path and instance.origin is start:
            this_flight = instance.flight
            time_taken = cumulative_time + this_flight.duration
            if path:
                prev_flight = path[-1].flight
                transit_time = difference_time(
                    prev_flight.arrival, this_flight.departure
                )
                time_taken += transit_time
            elif instance.date != depature:
                continue
            
            if time_taken < limit:
                dest = instance.destination
                if dest is target:
                    yield FlightItinerary(*path, instance)

                else:
                    yield from _path_algorithm(
                        *path, instance, 
                        start = dest,
                        target = target, 
                        pool = pool, 
                        limit = limit
                    )