"""
"""
from __future__ import annotations
from app.base import *

if TYPE_CHECKING:
    from . import Aircraft, Flight, Fare
    

class Deviation:
    """
    ### A exception to a FlightPlan
    
    - `weekdays`: `set(int)`
        - 0 <= weekday <= 6
        
    - `months`: `set(int)`
        - 1 <= month <= 12
    """
    def __init__(self, 
        weekdays: Optional[Iterable[int]] = None, 
        months: Optional[Iterable[int]] = None,
        dates: Optional[Iterable[dt.date]] = None,
    ):
        self.__weekdays = set(weekdays or [])
        self.__months = set(months or [])
        self.__dates = set(dates or [])
    
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


class FlightPlan:
    """
    A plan which tell what Flight will be available (operated) 
    on what period of time or range of dates
    """
    def __init__(self,
        flight: Flight,
        start: dt.date,
        end: dt.date = dt.date.max,
        exception: Optional[Deviation] = None,
        *,
        default_aircraft: Aircraft,
        default_fares: Sequence[tuple[TravelClass, Fare]],
    ):
        self.__flight = flight
        self.__start = start
        self.__end = end
        self.__exception = exception or Deviation()
        self.__default_aircraft = default_aircraft
        self.__default_fares = tuple(default_fares)
    
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
    def default_aircraft(self):
        return self.__default_aircraft

    @property
    def default_fares(self):
        return self.__default_fares
    
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