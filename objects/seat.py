"""
seat
"""
from __future__ import annotations
from base import *

Class = Enum(
    'Travel Class', 
    'FIRST BUSINESS ECONOMY'
)

@dataclass
class SeatType:
    cls: Class
    name: str # standard, comfort, elite, convenience, etc.
    price: int
    information: InfoType # lie flat 180 degree recline, checked baggage: 2 pieces, 23 kg each, hand baggage ... pitch, width


@dataclass
class SeatPostion:
    row: int
    column: int
    
    def __post_init__(self):
        self.column = chr(self.column + 64)
    
    def __str__(self):
        return f'{self.row}{self.column}'
    

@dataclass
class Seat:
    type: SeatType
    position: SeatPostion
    
    @property
    def id(self):
        return str(self.position)
    
    @property
    def price(self):
        return self.type.price