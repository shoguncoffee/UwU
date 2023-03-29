from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from .seat import Seat

@dataclass(init=False, slots=True, unsafe_hash=True)
class Desk:
    __cabins: tuple[CabinLayout, ...] # type: ignore

    def __init__(self, *cabin: CabinLayout):
        self.__cabins = cabin
    
    @property
    def cabins(self):
        return self.__cabins

    def get_seats(self):
        """
        get all passenger's seat in this desk
        """
        return set(
            seat for cabin in self.cabins
            for seat in cabin.seats
        )


@dataclass(slots=True, frozen=True)
class CabinLayout:
    __class_type: TravelClass # type: ignore
    __seats: frozenset[Seat] # type: ignore
    
    @property
    def class_type(self):
        return self.__class_type

    @property
    def seats(self):
        return self.__seats