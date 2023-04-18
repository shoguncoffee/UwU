from __future__ import annotations
from ..base import *

if TYPE_CHECKING:
    from app.src import FlightInstance, Booking, PassengerDetails, Seat


@dataclass(slots=True)
class FlightReservation:
    __instance: FlightInstance # type: ignore
    __travel_class: TravelClass # type: ignore
    __holder: Booking # type: ignore
    
    __selected: Optional[tuple[SeatReservation]] = field(init=False, default=None)

    @property
    def flight(self):
        return self.__instance
    
    @property
    def travel_class(self):
        return self.__travel_class
    
    @property
    def holder(self):
        return self.__holder
    
    @property
    def selected(self):
        """
        selected seats
        """
        return self.__selected
    
    def select_seats(self, selected: Iterable[SeatReservation]):
        selected = tuple(selected)
        passengers = {
            select.passenger for select in selected
        }
        if passengers == set(self.holder.passengers):
            self.__selected = selected
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