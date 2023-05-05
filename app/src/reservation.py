from __future__ import annotations
from app.base import *

if TYPE_CHECKING:
    from . import Booking, FlightClass, Passenger, Seat


class FlightReservation:
    def __init__(self, holder: Booking, provider: FlightClass):
        self.__holder = holder
        self.__provider = provider
        self.__selected = tuple(
            SeatReservation(passenger) 
            for passenger in holder.passengers
        )
        self.__is_assigned = False
    
    @property
    def holder(self):
        return self.__holder
    
    @property
    def provider(self):
        return self.__provider
    
    @property
    def is_assigned(self):
        return self.__is_assigned
    
    @property
    def selected(self):
        """
            selected seats
        """
        return self.__selected
    
    def assign_seats(self, 
        selected: Optional[Iterable[SeatReservation]] = None
    ):
        selected = tuple(selected) if selected else self.selected
        passengers = {
            select.passenger for select in selected
        }
        if passengers == set(self.holder.passengers):
            self.__selected = selected
            self.__is_assigned = True
            return True


@dataclass
class SeatReservation:
    __passenger: Passenger # type: ignore
    __seat: Optional[Seat] = None # type: ignore

    @property
    def passenger(self):
        return self.__passenger

    @property
    def seat(self):
        return self.__seat