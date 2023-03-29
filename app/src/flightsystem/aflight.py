"""
take care of flight system
"""
from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from ..ArthurWork import Aircraft, Airport
    from ..booking_related import FlightReservation
    from ..constants import FlightStatus, BookingStatus

class FlightCatalog(Singleton):
    _instance: FlightCatalog
    
    def __init__(self):
        self.__record: set[Flight] = set()
    
    @property
    def record(self):
        return self.__record
    
    @classmethod
    def add(cls, flight: Flight):
        cls._instance.__record.add(flight)
    
    @classmethod
    def search(cls, designator: str):
        ...


@dataclass
class Flight: #(HasReference):
    __designator: str # type: ignore
    __departure: time # type: ignore
    __arrival: time # type: ignore
    __origin: Airport # type: ignore
    __destination: Airport # type: ignore
    # __reference: Optional[UUID] = None # type: ignore
    
    def __post_init__(self):
        self.__designator = self.designator.upper()
        # self.__reference = self.__reference or self.generate_reference()
    
    @property
    def designator(self):
        return self.__designator
    
    @property
    def departure(self):
        return self.__departure
    
    @property
    def arrival(self):
        return self.__arrival
    
    @property
    def origin(self):
        return self.__origin
    
    @property
    def destination(self):
        return self.__destination
    
    @property
    def duration(self) -> timedelta:
        crossday = timedelta(self.__arrival < self.__departure)
        d2 = datetime.combine(date.min + crossday, self.__arrival)
        d1 = datetime.combine(date.min, self.__departure)
        return d2 - d1
    
    @classmethod
    def generate_reference(cls):
        return 
    
    
@dataclass
class FlightInstance:
    __flight: Flight # type: ignore
    __date: date # type: ignore
    __aircraft: Aircraft # type: ignore
    __base_price: float # type: ignore
    __booking_record: set[FlightReservation] = field_set # type: ignore
    __status: FlightStatus = FlightStatus.SCHEDULED # type: ignore
    
    @property
    def flight(self):
        return self.__flight
    
    @property
    def date(self):
        return self.__date
    
    @property
    def aircraft(self):
        return self.__aircraft
    
    @property
    def booking_record(self):
        return self.__booking_record
    
    @property
    def status(self):
        return self.__status
    
    @property
    def designator(self):
        return self.flight.designator
    
    def update_status(self, status: FlightStatus):
        self.__status = status
    
    def get_reserved_seats(self):
        """
        get all reserved seats that have be paid (reservation status is confirmed)
        """
        return set(
            seat for reservation in self.get_comfirmed()
            for seat in reservation.seats
        )
        
    def get_available_seats(self):
        ...
        
    def get_comfirmed(self):
        """
        get all confirmed reservations
        """
        return set(
            reservation for reservation in self.__booking_record 
            if reservation.holder.status == BookingStatus.COMPLETE
        )