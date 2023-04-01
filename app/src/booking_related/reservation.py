from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from app.src import *

@dataclass(slots=True, unsafe_hash=True)
class FlightReservation:
    __flight: FlightInstance # type: ignore
    __travel_class: TravelClass # type: ignore
    __holder: Booking # type: ignore
    
    __reservation: Optional[tuple[SeatReservation]] = field(init=False, hash=False, default=None)

    @property
    def flight(self):
        return self.__flight
    
    @property
    def travel_class(self):
        return self.__travel_class
    
    @property
    def holder(self):
        return self.__holder
    
    @property
    def reservation(self):
        return self.__reservation or ()

    @property
    def is_selected(self):
        """
        True if seats has been selected
        """
        return self.reservation is not None
    
    
    def select_seat(self, selected: tuple[SeatReservation]):
        if self.holder and len(selected) == self.holder.pax:
            self.__reservation = selected
            return True


@dataclass(slots=True)
class SeatReservation:
    __passenger: PassengerDetails # type: ignore
    __seat: Optional[Seat] # type: ignore

    @property
    def passenger(self):
        return self.__passenger

    @property
    def seat(self):
        return self.__seat