from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from ..flightsystem import FlightInstance
    from .booking import Booking
    from .seat_reservation import SeatReservation

@dataclass(slots=True, unsafe_hash=True)
class FlightReservation:
    __flight: FlightInstance # type: ignore
    __class_of_service: TravelClass # type: ignore
    __holder: Booking # type: ignore
    
    __seats: Optional[tuple[SeatReservation]] = field(init=False, hash=False, default=None) # type: ignore

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
        return self.__seats or []

    @property
    def is_selected(self):
        """
        True if seats has been selected
        """
        return self.seats is not None
    
    @property
    def is_booking(self):
        """
        True if ...
        """
        return self.holder is not None
    
    
    def select_seat(self, selected: tuple[SeatReservation]):
        if self.holder and len(selected) == self.holder.passenger_number:
            self.__seats = selected
            return True
    
    def init_holder(self, holder: Booking):
        self.__holder = holder