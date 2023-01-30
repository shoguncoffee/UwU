from base import *

@dataclass
class Seat:
    pitch: int
    width: int
    lie_flat: bool # 180 degree recline
    
class Economy(Seat):
    ...


class Business(Seat):
    ...
    
    
class First(Seat):
    ...
    
