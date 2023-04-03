"""
"""
from __future__ import annotations
from ..base import *

if TYPE_CHECKING:
    from app.src import Flight
    
    
@dataclass(slots=True)
class Deviation:
    """
    A exception to a FlightPlan

        - 0 <= weekday <= 6
        - 1 <= month <= 12
    """
    __weekdays: set[int] = field(default_factory=set) # type: ignore
    __months: set[int] = field(default_factory=set) # type: ignore
    __dates: set[date] = field(default_factory=set) # type: ignore
    
    def __contains__(self, d: date):
        return (
            d.weekday() in self.weekdays
            or d.month in self.months
            or d in self.dates
        )
    
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
    """
    A plan which tell what Flight will be available (operated) 
    on what period of time or range of dates
    """
    __flight: Flight # type: ignore
    __start: date # type: ignore
    __end: date = date.max # type: ignore
    __exception: Deviation = field(default_factory=Deviation) # type: ignore
    
    _: KW_ONLY
    default_aircraft: Aircraft # type: ignore
    default_fare: float # type: ignore
    
    def __contains__(self, value: date | FlightPlan):
        """
        value: date
            check if it is in the range of this plan
        
        value: FlightPlan
            check if it is overlapping with this plan
        """
        if isinstance(value, date):
            return (
                self.start <= value <= self.end
                and value not in self.exception
            )
        if isinstance(value, FlightPlan):
            if (
                value.start > self.end or 
                self.start > value.end
            ):
                return False
            
            base = set(self.get_dates())
            for _date in value.get_dates():
                if _date in base:
                    return True
                
            return False
    
    
    @property
    def flight(self):
        return self.__flight
    
    @property
    def start(self):
        return self.__start
    
    @property
    def end(self):
        return self.__end
    
    @property
    def exception(self):
        return self.__exception

    @property
    def duration(self):
        return self.end - self.start
    
    def get_dates(self):
        days = self.duration.days
        for date in daterange(days, self.start):
            if date not in self.exception:
                yield date
    
    
    def scheduled(self):
        from app.system import Airline
        Airline.plans.add(self)