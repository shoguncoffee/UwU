from __future__ import annotations
from ..base import *
from ..info import Information

@dataclass(slots=True, frozen=True)
class Seat:
    __row: int # type: ignore
    __column: int # type: ignore
    __type: SeatType # type: ignore
    __description: Information = field(hash=False, default_factory=Information) # type: ignore
    
    @property
    def row(self):
        return self.__row
    
    @property
    def column(self):
        return self.__column
    
    @property
    def type(self):
        return self.__type
    
    @property
    def description(self):
        return self.__description