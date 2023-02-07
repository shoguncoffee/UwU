"""
aircraft
"""
from __future__ import annotations
from base import *
if TYPE_CHECKING:
    import seat
    import airport

AVARAGE_SPEED = 700

@dataclass
class Aircraft:
    """
    Aircraft specifications
    """
    model: str
    layout: tuple[Layout, ...]
    max_range: int
    speed: int = AVARAGE_SPEED
    information: InfoType = InfoType()
    
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
    space: set[tuple[int, int]]
    
    @property
    def capacity(self, type: Optional[seat.Class] = None):
        n = self.column_width * sum(self.row_class)
        
        return n - len(self.space)
    
    
    # self.column_width * row_class[0]
    # self.column_width * row_class[1]
    # self.column_width * row_class[3]