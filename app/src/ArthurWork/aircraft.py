from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from .cabin_layout import CabinLayout
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Aircraft:
    __model: str # type: ignore
    __cabins: tuple[CabinLayout] # type: ignore
    
    @property
    def model(self):
        return self.__model
    
    @property
    def cabins(self):
        return self.__cabins
    
    def get_seats(self):
        """
        get all passenger seat in the aircraft
        """
        return set(
            seat for cabin in self.cabins
            for seat in cabin.seats
        )
        
    def get_layout(self):
        pass