"""
"""
from __future__ import annotations
from .base import *

if TYPE_CHECKING:
    from . import *
    
    
@dataclass(slots=True)
class Deviation:
    """
    ### A exception to a FlightPlan
    
    - `weekdays`: `set(int)`
        - 0 <= weekday <= 6
        
    - `months`: `set(int)`
        - 1 <= month <= 12
    """
    __weekdays: set[int] = field(default_factory=set) # type: ignore
    __months: set[int] = field(default_factory=set) # type: ignore
    __dates: set[dt.date] = field(default_factory=set) # type: ignore
    
    def __contains__(self, date: dt.date):
        """
        check if date overlapping with this Deviation
        """
        return (
            date.weekday() in self.weekdays
            or date.month in self.months
            or date in self.dates
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
    __start: dt.date # type: ignore
    __end: dt.date = dt.date.max # type: ignore
    __exception: Deviation = field(default_factory=Deviation) # type: ignore
    
    _: KW_ONLY
    default_aircraft: Aircraft
    default_fares: fares_param 
    
    def __contains__(self, value: dt.date | Self):
        """
        - `value`: `dt.date`
            - check if it is in the range of this plan
        - `value`: `FlightPlan`
            - check if it is overlapping with this plan
        """
        if isinstance(value, dt.date):
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
            for date in value.get_dates():
                if date in base:
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