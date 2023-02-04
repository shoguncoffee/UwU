from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from seat import Seat
    from airport import Airport

@dataclass
class Aircraft:
    """
    Aircraft Specifications
    """
    model: str
    layout: list[Layout]
    information: list[str]
    
    @property
    def capacity(self):
        return sum(layout.capacity for layout in self.layout)
    
    #@property
    #def u(self):
    #    return sum(self.seats)
    
@dataclass 
class Layout:
    """
       |-------| => column_width
       A B C D E
    1) x x x x x - first class (1)
    
    2) x x x x x -
    3) x x x x x - business class (2)
    
    4) x x x x x -
    5) x x x x x | economy class (3)
    6) x x x x x - 
    """
    column_width: int
    row_class: tuple[int, int, int] # first, business, economy
    position_exception: list[tuple[int, int]]
    
    @property
    def capacity(self):
        n = self.column_width * sum(self.row_class)
        return n - len(self.except_position)
    
    
    self.column_width * row_class[0] -> จำนวน first
    self.column_width * row_class[1] -> จำนวน buss
    self.column_width * row_class[3] -> จำนวน eco