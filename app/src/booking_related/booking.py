from __future__ import annotations
from ..base import *

from dataclasses import InitVar
from .reservation import FlightReservation
if TYPE_CHECKING:
    from app.src import *


@dataclass(slots=True)
class Booking:
    __datetime: datetime = field(init=False, default_factory=datetime.now)
    
    __creator: Customer # type: ignore
    __journey: InitVar[list[Trip]] # type: ignore
    __contactinfo: ContactInformation # type: ignore
    __passenger: tuple[PassengerDetails, ...] # type: ignore
    
    __reservation: tuple[FlightReservation, ...] = field(init=False)
    __payment: Optional[Payment] = field(init=False, default=None)
    __status: BookingStatus = field(init=False, default=BookingStatus.INCOMPLETE)

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