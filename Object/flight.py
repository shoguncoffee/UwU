from base import *
if TYPE_CHECKING:
    from aircraft import Aircraft
    from airport import Airport

STATUS = Enum('Flight Status', 
    'SCHEDULED CANCLE'
)

@dataclass
class Flight:
    code: str
    aircraft: Aircraft
    origin: Airport
    destination: Airport
    departure: datetime
    arrival: datetime
    status = STATUS
    
    def __post_init__(self):
        ...
    
    @property
    def travel_time(self):
        return 
    
    @property
    def passenger(self):
        return sum()
   
    
if __name__ != '__main__':
    globals().update(STATUS.__members__)
    