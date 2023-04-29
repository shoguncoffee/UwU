"""
system
"""
from __future__ import annotations
from app.base import *

from app.src import *
from app.type_alias import journey_param


class Airline:
    """
    ### represent the system of this project
    
        initialize system by:
        >>> Airline()
    """
    name = 'Qatar Airways'
    designator = 'QR'
    path = 'test-run'
    
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
    def dump(cls):
        """
        """
        with open(cls.path, 'wb') as f:
            pickle.dump(cls._instance, f)
    
    @classmethod
    def load(cls):
        """
        """
        with open(cls.path, 'rb') as f:
            obj = pickle.load(f)

        print(obj)
        cls._instance = obj
    
    @classmethod
    def create_booking(cls,
        creator: Customer,
        contact: ContactInformation,
        passengers: Sequence[Passenger],
        journey: journey_param
    ):
        pax = Pax.init(passengers)
        if all(
            itinerary.bookable(pax, travel_class) 
            for itinerary, travel_class in journey
        ):
            booking = Booking(
                creator,
                contact,
                tuple(passengers),
                journey,
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
        selected: list[tuple[Passenger, Seat]],
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
    ): 
        """
        return a list of FlightItinerary by any possible FlightInstance
        that can take from origin to destination in limit duration
            - limit: `datetime.timedelta`
                - maximum flight time of the path (not including transit time)
        """
        from .utils import algorithm
        
        searcher = algorithm.SearchHelper(
            origin, destination, date, [
                *chain.from_iterable(
                    cls.schedules.get(day) for day in daterange(2, date)
                )
            ],
        )
        filtered = [
            *filter(lambda i: i.bookable(pax), searcher)
        ]
        unique_departure = {
            itinerary.departure for itinerary in filtered
        }
        per_departure = [
            sorted(
                filter(lambda i: i.departure == departure, filtered)
            ) for departure in unique_departure
        ]
        return sorted(cheaper for cheaper, *_ in per_departure)