"""
"""
from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from src import Flight, ScheduleCatalog
    

class FlightScheduling:
    __plans: set[Flight] #type: ignore
    __advance_days: int = 365 #type: ignore
    
    @classmethod
    def add(self, plan: FlightPlan):
        self.__plans.add(plan)
    
    
@dataclass    
class FlightPlan:
    __flight: Flight # type: ignore
    __start_date: date # type: ignore
    __end_date: Optional[date] = None # type: ignore
    __exception: Deviation # type: ignore
    
    @property
    def duration(self):
        """
        if not have end date, return None
        """
        if self.__end_date is not None:
            return self.__end_date - self.__start_date
        
        return None
    
    def scheduled(self):
        FlightScheduling.add(self)
    

@dataclass    
class Deviation:
    __weekdays: set[int] # type: ignore
    __months: set[int] # type: ignore
    __dates: set[date] # type: ignore