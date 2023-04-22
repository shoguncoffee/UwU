"""
system
"""
from .base import *
from .src import *
from .src.catalog import *
from .utils import algorithm

class Airline:
    """
    ### represent the system of this project
    
    initialize system by:
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
        journey: journey_param,
        contact: ContactInformation,
        passengers: Sequence[PassengerDetails],
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
                tuple(passengers),
            )
            for reservation in booking.all_reservations:
                flightclass = reservation.provider
                flightclass.booked(reservation)
            
            creator.bookings.append(booking)
            booking.pending()
            return True
    
    
    @classmethod
    def select_seats(cls, 
        reservation: FlightReservation,
        selected: list[tuple[PassengerDetails, Seat]],
    ):
        flightclass = reservation.provider
        
        if flightclass.bookable(reservation.holder.pax):
            occupied = flightclass.get_occupied_seats()
            
            if not occupied.intersection(seat for _, seat in selected):
                return reservation.assign_seats(
                    SeatReservation(*select) for select in selected
                )
    
    
    @classmethod
    def payment(cls, 
        booking: Booking,
        payment_method: PaymentMethod,
    ):
        if not booking.payment:
            payment = payment_map[payment_method].pay(booking)
            ...
    
    
    @classmethod
    def register(cls, account: Account):
        if account not in cls.accounts:
            cls.accounts.append(account)
            return True
            
    @classmethod
    def login(cls, username: str, password: str):
        account = cls.accounts.get(username)
        return account.hash_password == hash(password)
    
    @classmethod
    def search_journey(cls,
        origin: Airport, 
        destination: Airport, 
        date: dt.date,
        pax: Pax = Pax(),
        duration_cutoff: dt.timedelta = dt.timedelta(hours=30),
    ): 
        """
        return a list of FlightItinerary by any possible FlightInstance
        that can take from origin to destination in limit duration
        """
        pool = [
            instance for day in daterange(duration_cutoff.days, date)
            for instance in Airline.schedules.get(day)
        ]
        possible_itinerarys = (
            FlightItinerary(instances)
            for first in Airline.schedules.get(date) 
                if first.flight.origin is origin
                    for instances in algorithm.conjugate(
                        first,
                        target=destination,
                        pool=pool,
                        limit=duration_cutoff,
                    ) 
        )
        return sorted(
            [itinerary for itinerary in possible_itinerarys if itinerary.bookable(pax)], 
            key=lambda itinerary: itinerary.lowest_fare()
        )