from __future__ import annotations
from app.base import *

from .reservation import FlightReservation
from .passenger import Pax
if TYPE_CHECKING:
    from . import Customer, ContactInformation, Passenger, Payment, FlightItinerary


class Booking:
    def __init__(self, 
        creator: Customer,
        contact: ContactInformation,
        passengers: Sequence[Passenger],
        journey: Sequence[tuple[FlightItinerary, TravelClass]],
    ):
        self.__reference = uuid4()
        self.__datetime = dt.datetime.now()
        self.__status = BookingStatus.INCOMPLETE
        self.__payment: Optional[Payment] = None

        self.__creator = creator
        self.__contact = contact
        self.__passengers = tuple(passengers)
        self.__reservations = tuple(
            tuple(
                FlightReservation(self, instance.get_class(travel_class)) for instance in itinerary
            ) for itinerary, travel_class in journey 
        )
    
    @property
    def datetime(self):
        return self.__datetime
    
    @property
    def creator(self):
        return self.__creator
                
    @property
    def reservations(self):
        return self.__reservations
    
    @property
    def all_reservations(self):
        return [
            reservation for segment in self.reservations 
            for reservation in segment
        ]
    
    @property
    def passengers(self):
        return self.__passengers
    
    @property
    def reference(self):
        return self.__reference
    
    @property
    def contact(self):
        return self.__contact
        
    @property
    def payment(self):
        return self.__payment
    
    @property
    def status(self):
        return self.__status
    
    @property
    def creation_time(self):
        return self.__datetime
    
    def get_pax(self):
        pax = Pax.count(self.passengers)
        return pax

    def update_payment(self, payment: Payment):
        self.__payment = payment
        self.__status = BookingStatus.COMPLETED
        
    def cancel(self):
        self.__status = BookingStatus.CANCELLED
        
    def pending(self):
        self.__status = BookingStatus.PENDING        

    def get_price(self):
        prices: list[int] = []
        for reservation in self.all_reservations:
            fare = reservation.provider.fare
            prices.extend(
                fare.get_price(
                    selected.passenger.type, 
                    selected.seat and selected.seat.type
                ) for selected in reservation.selected
            )
        return sum(prices)