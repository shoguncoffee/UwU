from __future__ import annotations
from base import *

@dataclass
class Seat:
    row: int
    column: str
    price: int
        
    pitch: int
    width: int
    information: list[str]
    #-> lie flat 180 degree recline
    
class Economy(Seat):
    price: int = 


class Business(Seat):
    price: int = 
    
    
class First(Seat):
    
    
