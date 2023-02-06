"""
seat
"""
from __future__ import annotations
from base import *

CLASS = Enum(
    'Travel Class', 
    'FIRST BUSINESS ECONOMY'
)

@dataclass
class SeatType:
    name: str # standard, comfort, elite, convenience, etc.
    cls: CLASS
    price: int
    pitch: float
    width: float
    information: InfoType # lie flat 180 degree recline, checked baggage: 2 pieces, 23 kg each, hand baggage ...

@dataclass
class SeatPostion:
    row: int
    column: int
    
    

@dataclass
class Seat:
    type: SeatType
    row: int
    column: str

    
    
    @property
    def id(self):
        return f'{self.row}{self.column.upper()}'
    
    @property
    def price(self):
        return self.type.price