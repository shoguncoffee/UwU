from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from .seat import Seat
from dataclasses import dataclass
         
@dataclass(slots=True, frozen=True)
class CabinLayout:
    __desk: int # type: ignore
    __class_type: TravelClass # type: ignore
    __seats: set[Seat] # type: ignore

    @property
    def desk(self):
        return self.__desk
    
    @property
    def class_type(self):
        return self.__class_type

    @property
    def seats(self):
        return self.__seats