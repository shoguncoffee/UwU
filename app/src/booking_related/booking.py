from __future__ import annotations
from ..base import *

from dataclasses import InitVar
from .reservation import FlightReservation
if TYPE_CHECKING:
    from app.src import *


@dataclass(slots=True)
class Booking:
    __datetime: dt.datetime = field(init=False, default_factory=dt.datetime.now)
    
    __creator: Customer # type: ignore
    journey: InitVar[list[tuple[FlightItinerary, TravelClass]]]
    __contactinfo: ContactInformation # type: ignore
    __passengers: tuple[PassengerDetails, ...] # type: ignore
    
    __reference: UUID = field(init=False, default_factory=uuid4) # undone
    __reservations: tuple[FlightReservation, ...] = field(init=False)
    __payment: Optional[Payment] = field(init=False, default=None)
    __status: BookingStatus = field(init=False, default=BookingStatus.INCOMPLETE)

    def __post_init__(self, journey: list[tuple[FlightItinerary, TravelClass]]):
        self.__reservations = tuple(
            FlightReservation(flight, travel_class, self) 
            for itinerary, travel_class in journey 
            for flight in itinerary
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
    def passengers(self):
        return self.__passengers
    
    @property
    def reference(self):
        return self.__reference
    
    @property
    def contactinfo(self):
        return self.__contactinfo
        
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
        for reservation in self.reservations:
            fare = reservation.flight.get_fare(reservation.travel_class)
            if reservation.selected:
                prices.extend(
                    fare.get_price(
                        selected.passenger.type, 
                        selected.seat and selected.seat.type
                    ) for selected in reservation.selected
                )
            else:
                prices.extend(
                    fare.get_price(passenger.type) 
                    for passenger in self.passengers
                )   
        return sum(prices)