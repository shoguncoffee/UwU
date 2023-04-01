from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from app.src import *
from dataclasses import InitVar
from .reservation import FlightReservation

@dataclass(slots=True, unsafe_hash=True)
class Booking: #(HasReference):
    __datetime: datetime = field(init=False, default_factory=datetime.now)
    # __reference: Optional[UUID] = reference or self.generate_reference() # type: ignore
    
    __creator: Customer = field(hash=False) # type: ignore
    __journey: InitVar[list[Trip]] # type: ignore
    __contactinfo: ContactInformation = field(hash=False) # type: ignore
    __passenger: tuple[PassengerDetails, ...] = field(hash=False) # type: ignore
    
    __reservation: tuple[FlightReservation, ...] = field(init=False, hash=False)
    __payment: Optional[Payment] = field(init=False, hash=False, default=None)
    __status: BookingStatus = field(init=False, hash=False, default=BookingStatus.INCOMPLETE)

    def __post_init__(self, journey: list[Trip]):
        self.__reservation = tuple(
            FlightReservation(flight, trip.travel_class, self) 
            for trip in journey for flight in trip.flights
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
    def pax(self):
        return len(self.passenger)
    
    def cancel(self):
        self.__status = BookingStatus.CANCELLED
        
    def pending(self):
        self.__status = BookingStatus.PENDING