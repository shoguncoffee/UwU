"""
"""
from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from .aflight import Flight

class FlightScheduling:
    _instance: FlightScheduling 
    
    def __init__(self, advance_days: int = 365):
        self.__advance_days = advance_days
        self.__plans: list[FlightPlan] = []
    
    @property
    def advance_days(self):
        return self.__advance_days
    
    @property
    def plans(self):
        return self.__plans
    
    @classmethod
    def add(cls, plan: FlightPlan):
        cls._instance.__plans.append(plan)
    

@dataclass(slots=True)
class Deviation:
    __weekdays: set[int] = field(default_factory=set) # type: ignore
    __months: set[int] = field(default_factory=set) # type: ignore
    __dates: set[date] = field(default_factory=set) # type: ignore
    
    @property
    def weekdays(self):
        return self.__weekdays
    
    @property
    def months(self):
        return self.__months
    
    @property
    def dates(self):
        return self.__dates
    

@dataclass(slots=True)
class FlightPlan:
    __flight: Flight # type: ignore
    __start_date: date # type: ignore
    __end_date: Optional[date] = None # type: ignore
    __exception: Deviation = field(default_factory=Deviation) # type: ignore
    
    @property
    def flight(self):
        return self.__flight
    
    @property
    def start_date(self):
        return self.__start_date
    
    @property
    def end_date(self):
        return self.__end_date
    
    @property
    def exception(self):
        return self.__exception
    
    @property
    def duration(self):
        """
        if not have end date, return None
        """
        if self.__end_date:
            return self.__end_date - self.__start_date
        
    
    def scheduled(self):
        FlightScheduling.add(self)