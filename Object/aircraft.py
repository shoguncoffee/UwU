from base import *
from airport import Airport
if TYPE_CHECKING:
    from seat import Seat

@dataclass
class Aircraft:
    model: str
    seats: list[Seat]
    info: dict
    #crew: int
    
    @property
    def capacity(self):
        return len(self.seats)
    
    def go_to(self, destination: Airport):
        ...
    
    