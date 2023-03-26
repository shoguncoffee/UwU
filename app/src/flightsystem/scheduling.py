"""
"""
from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from src import ScheduleCatalog
    from src.flightsystem import Flight
    

class FlightScheduling(Singleton):
    __advance_days: int = 365 #type: ignore
    _instance: FlightScheduling 
    
    def __init__(self):
        self.__plans: set[FlightPlan] = set()
        
    @classmethod
    def add(cls, plan: FlightPlan):
        cls._instance.__plans.add(plan)
    

@dataclass    
class Deviation:
    __weekdays: set[int] = field_set # type: ignore
    __months: set[int] = field_set # type: ignore
    __dates: set[date] = field_set # type: ignore
    

@dataclass    
class FlightPlan:
    __flight: Flight # type: ignore
    __start_date: date # type: ignore
    __end_date: Optional[date] = None # type: ignore
    __exception: Deviation = field(default_factory=Deviation) # type: ignore
    
    @property
    def duration(self):
        """
        if not have end date, return None
        """
        if self.__end_date:
            return self.__end_date - self.__start_date
        
    
    def scheduled(self):
        FlightScheduling.add(self)