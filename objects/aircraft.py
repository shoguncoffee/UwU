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
    seats: tuple[int, int, int]
    information: list[str]
    
    @property
    def capacity(self):
        return sum(self.seats)
    
    @property
    def (self):
        return sum(self.seats)