from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from .passenger_detail import PassengerDetails
    from ..ArthurWork.seat import Seat

@dataclass
class SeatReservation:
    __passenger: PassengerDetails # type: ignore
    __seat: Optional[Seat] # type: ignore

    @property
    def passenger(self):
        return self.__passenger

    @property
    def seat(self):
        return self.__seat