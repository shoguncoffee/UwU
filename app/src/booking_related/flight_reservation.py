from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from ..flightsystem import FlightInstance
    from .booking import Booking
    from .seat_reservation import SeatReservation

@dataclass
class FlightReservation:
    __flight: FlightInstance # type: ignore
    __class_of_service: TravelClass # type: ignore
    __holder: Optional[Booking] = None # type: ignore
    __seats: set[SeatReservation] | None = field(init=False, default=None) # type: ignore

    @property
    def flight(self):
        return self.__flight
    
    @property
    def class_of_service(self):
        return self.__class_of_service
    
    @property
    def holder(self):
        return self.__holder
    
    @property
    def seats(self):
        return self.__seats

    @property
    def is_selected(self):
        return self.seats is not None
    
    
    def select_seat(self, selected: set[SeatReservation]):
        if len(selected) == self.holder.passenger_number:
            self.__seats = selected
            return True