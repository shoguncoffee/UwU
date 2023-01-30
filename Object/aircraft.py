from base import *
from airport import Airport

@dataclass
class Aircraft:
    model: str
    seats: int
    crew: int
    
    Manufacturer: str
    
    def go_to(self, destination: Airport):
        ...
    