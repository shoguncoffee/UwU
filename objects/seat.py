from __future__ import annotations
from base import *

@dataclass
class Seat:
    type: SeatType
    row: int
    column: str

    pitch: int
    width: int
    information: list[str]
    #-> lie flat 180 degree recline
    
    @property
    def id(self):
        return f'{self.row}{self.column.upper()}'
    
    @property
    def price(self):
        return self.type.price
    
@dataclass
class SeatType:
    name: str
    price: int