"""
system
"""
from __future__ import annotations
from .base import *
from .src import *

class Airline:
    """
    ### represent the system of this project
    
    init system
    >>> Airline()
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
        journey: list[tuple[FlightItinerary, TravelClass]],
        contact: ContactInformation,
        *passengers: PassengerDetails,
    ):
        pax = Pax.init(passengers)
        if all(
            itinerary.bookable(pax, travel_class) 
            for itinerary, travel_class in journey
        ):
            booking = Booking(
                creator,
                journey,
                contact,
                passengers,
            )
            for reservation in booking.reservations:
                flight = reservation.flight
                flight.booked(reservation)
                
            creator.add_booking(booking)
            booking.pending()
            return True
    
    
    @classmethod
    def select_seats(cls, 
        reservation: FlightReservation,
        selected: list[tuple[PassengerDetails, Seat]],
    ):
        instance = reservation.flight
        occupied = instance.get_occupied_of(
            reservation.travel_class
        )
        if not occupied.intersection(seat for _, seat in selected):
            return reservation.select_seats(
                SeatReservation(*select) for select in selected
            )
    
    
    @classmethod
    def pay(cls, 
        booking: Booking,
        payment: Payment,
    ):
        
        return ...
    
    
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
        date: dt.date,
        pax: Pax = Pax(),
        duration_cutoff: dt.timedelta = dt.timedelta(hours=17),
    ): 
        """
        return a list of FlightItinerary by any possible FlightInstance
        that can take from origin to destination in limit duration
        """
        possible_instance: list[FlightInstance] = []
        for _date in daterange(duration_cutoff.days, date):
            schedule = Airline.schedules.get(_date)
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
            key = lambda itinerary: itinerary.lowest_fare()
        )
        return result
        
        
def _path_algorithm(
    *path: FlightInstance, 
    start: Airport,
    target: Airport,
    pool: Sequence[FlightInstance],
    limit: dt.timedelta,
    depature: Optional[dt.date] = None,
) -> Generator[FlightItinerary, None, None]:
    
    cumulative_time = sum(
        [inst.flight.duration for inst in path], 
        start = dt.timedelta()
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
                    yield FlightItinerary([*path, instance])

                else:
                    yield from _path_algorithm(
                        *path, instance, 
                        start = dest,
                        target = target, 
                        pool = pool, 
                        limit = limit
                    )