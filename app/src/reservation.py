from __future__ import annotations
from .base import *


@dataclass(slots=True)
class FlightReservation:
    __holder: Booking # type: ignore
    __provider: FlightClass # type: ignore
    
    __selected: tuple[SeatReservation, ...] = field(init=False)
    __is_assigned: bool = field(init=False, default=False)

    def __post_init__(self):
        self.__selected = tuple(
            SeatReservation(passenger) for passenger in self.holder.passengers
        )
    
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


@dataclass(slots=True)
class SeatReservation:
    __passenger: PassengerDetails # type: ignore
    __seat: Optional[Seat] = None # type: ignore

    @property
    def passenger(self):
        return self.__passenger

    @property
    def seat(self):
        return self.__seat