from __future__ import annotations
from app.base import *

from dataclasses import InitVar
from .reservation import FlightReservation
from .passenger import Pax
if TYPE_CHECKING:
    from . import *


@dataclass(slots=True)
class Booking:
    __creator: Customer # type: ignore
    __contact: ContactInformation # type: ignore
    __passengers: tuple[Passenger, ...] # type: ignore
    journey: InitVar[journey_param]
    
    __reservations: tuple[tuple[FlightReservation, ...], ...] = field(init=False)
    __payment: Optional[Payment] = field(init=False, default=None)
    __datetime: dt.datetime = field(init=False, default_factory=dt.datetime.now)
    __status: BookingStatus = field(init=False, default=BookingStatus.INCOMPLETE)
    __reference: UUID = field(init=False, default_factory=uuid4) #!

    def __post_init__(self, journey: journey_param):
        self.__reservations = tuple(
            tuple(
                FlightReservation(self, instance.get_class(travel_class)) 
                for instance in itinerary
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
        for segment in self.reservations:
            yield from segment
    
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
    
    @property
    def pax(self):
        return Pax.init(self.passengers)
    
    def cancel(self):
        self.__status = BookingStatus.CANCELLED
        
    def pending(self):
        self.__status = BookingStatus.PENDING
        
    def complete(self):
        self.__status = BookingStatus.COMPLETED
        
    def get_price(self):
        prices = []
        for reservation in self.all_reservations:
            fare = reservation.provider.fare
            prices.extend(
                fare.get_price(
                    selected.passenger.type, 
                    selected.seat and selected.seat.type
                ) for selected in reservation.selected
            )
        return sum(prices)