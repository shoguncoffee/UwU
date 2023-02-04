"""
seat
"""
from __future__ import annotations
from base import *

TYPE = Enum(
    'Travel Class', 
    'FIRST BUSINESS ECONOMY'
)

@dataslots
class SeatType:
    name: str # standard, elite
    type: TYPE
    price: int
    information: list[str] # lie flat 180 degree recline, checked baggage: 2 pieces, 23 kg each, hand baggage ...

@dataslots
class SeatPostion

@dataslots
class Seat:
    type: SeatType
    row: int
    column: str

    pitch: int
    width: int
    
    @property
    def id(self):
        return f'{self.row}{self.column.upper()}'
    
    @property
    def price(self):
        return self.type.price