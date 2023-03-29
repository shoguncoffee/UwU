from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from .customer import Customer
    from .passenger_detail import PassengerDetails
    from .contact_information import ContactInformation
    from ..K import Payment
    from ..ArthurWork.flight_itinerary import Trip
from dataclasses import InitVar
from .flight_reservation import FlightReservation

@dataclass(slots=True, unsafe_hash=True)
class Booking: #(HasReference):
    __datetime: datetime = field(init=False, default_factory=datetime.now)
    __reservation: tuple[FlightReservation, ...] = field(init=False, hash=False) # type: ignore
    # __reference: Optional[UUID] = reference or self.generate_reference() # type: ignore
    
    __journey: InitVar[list[Trip]] # type: ignore
    __creator: Customer = field(hash=False) # type: ignore
    __passenger: tuple[PassengerDetails, ...] = field(hash=False) # type: ignore
    __contactinfo: ContactInformation = field(hash=False) # type: ignore
    __payment: Optional[Payment] = field(init=False, hash=False, default=None) # type: ignore
    __status: BookingStatus = field(init=False, hash=False, default=BookingStatus.INCOMPLETE) # type: ignore

    def __post_init__(self, journey: list[Trip]):
        self.__reservation = tuple(
            FlightReservation(flight, trip.travel_class, self) 
            for trip in journey for flight in trip.itinerary.flights
        )

    @property
    def creator(self):
        return self.__creator
                
    @property
    def reservation(self):
        return self.__reservation
    
    @property
    def passenger(self):
        return self.__passenger
    
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
    def creation_datetime(self):
        return self.__datetime
    
    
    @property
    def is_completed(self):
        return self.status == BookingStatus.COMPLETED
    
    @property
    def is_connecting_flight(self):
        return len(self.reservation) > 1
    
    @property
    def passenger_number(self):
        return len(self.passenger)
    
    def cancel(self):
        self.__status = BookingStatus.CANCELLED