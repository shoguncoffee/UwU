"""
catalog
"""
from __future__ import annotations
from .base import *

from . import search
from app.src import (
    Account,
    Airport,
    Aircraft,
    Flight,
    FlightPlan,
    FlightInstance
)
__all__ = [
    'AccountCatalog',
    'AirportCatalog',
    'AircraftCatalog',
    'FlightCatalog',
    'FlightScheduling',
    'ScheduleCatalog',
    'ScheduleDate',
]    

class FlightScheduling(set[FlightPlan]):
    def __init__(self, advance_days: int = 365):
        self.__advance_days = advance_days
    
    @property
    def advance_days(self):
        return self.__advance_days
    
    def set_advance_days(self, days: int):
        self.__advance_days = days
        ...
    
    def search():
        ...


class ScheduleDate(set[FlightInstance]):
    def __init__(self, date: date) :
        self.__date = date
        
    def __hash__(self):
        return hash(self.date)
    
    def __eq__(self, value: ScheduleDate):
        return self.date == value.date

    @property
    def date(self):
        return self.__date


class ScheduleCatalog(set[ScheduleDate]):
    def delete_history(self):
        for schedule in self:
            pass
    
    def search(self, 
        date, 
        origin, 
        destination, 
        pax
    ):
        pass
    
    def get_possible_schedule(self, date):
        for schedule in self:
            pass
        
    def match_flight_itinerary_between_airport(self):
        pass
    
    
    def get_flight_instance(self, origin, destination):
        pass
    
    
class FlightCatalog(set[Flight]):
    def search(self, designator: str):
        return search('designator', designator, self)
    
    
class AirportCatalog(set[Airport]):
    def search(self, query: str):
        return search.multi_opt()


    
class AircraftCatalog(set[Aircraft]):
    def search(self):
        ...

    
class AccountCatalog(list[Account]):
    def __init__(self):
        self.__usernames: set[str] = set()
    
    def append(self, account: Account):
        self.__usernames.add(account.username)
        super().append(account)
        
    def remove(self, account: Account):
        self.__usernames.remove(account.username)
        super().remove(account)
        
    def __contains__(self, key):
        if isinstance(key, str):
            return key in self.__usernames  
        else:
            if isinstance(key, Account):
                if key.username not in self.__usernames:
                    return False
            
            return super().__contains__(key)
        
    def search(self, username: str):
        return search('username', username, self)


if __name__ == '__main__':
    q = AccountCatalog()
    class w:
        def __init__(self, x): self.username = x
        
    e = w('123')
    q.append(e)
    q.search('13')