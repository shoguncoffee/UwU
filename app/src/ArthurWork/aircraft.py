from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from .cabin_layout import Desk

@dataclass(init=False, slots=True, unsafe_hash=True)
class Aircraft:
    __model: str # type: ignore
    __desks: tuple[Desk, ...] # type: ignore
    
    def __init__(self, model: str, *desk: Desk):
        self.__model = model
        self.__desks = desk
    
    @property
    def model(self):
        return self.__model
    
    @property
    def desks(self):
        return self.__desks
    
    def get_seats(self):
        """
        get all passenger's seat in the aircraft
        """
        return set(
            seat for desk in self.desks
            for seat in desk.get_seats()
        )
        
    def get_cabins(self, desk_no: int):
        return self.desks[desk_no].cabins