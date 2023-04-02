"""
Catalog
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


class FlightScheduling(list[FlightPlan]): # may be dict[Flight, [Interval]]?
    """
    A tools to manage and organize flight in advance
        - keep continuity for the flight-booking system
        - ...
    """
    def __init__(self, advance_days: int = 365):
        self.set_advance_days(advance_days)
    
    @property
    def advance_days(self):
        return self.__advance_days
    
    def set_advance_days(self, days: int):
        self.__advance_days = days
        self.update()
    
    def update(self):
        for date in daterange(self.advance_days):
            schedule = ScheduleDate()
            for plan in self.on_date(date):
                schedule.add(
                    FlightInstance(date, 
                        plan.flight, 
                        plan.default_aircraft, 
                        plan.default_fare
                    )
                )
            from app.system import Airline
            Airline.schedules.add(date, schedule)
    
    def add(self, plan: FlightPlan):
        for p in self:
            if p.flight.designator == plan.flight.designator:
                if p in plan: break
        else:
            self.append(plan)
    
    def on_date(self, 
        date: date, 
        plans: Optional[list[FlightPlan]] = None
    ):
        for plan in plans or self:
            if date in plan:
                yield plan
    
    def search(self,
        date: Optional[date] = None,
        flight: Optional[Flight] = None,
    ) -> list[FlightPlan]:
        """
        search for FlighPlan of what flight, on what date (all by default)
        """
        results = self
        if flight:
            results = [
                plan for plan in results
                if plan.flight == flight
            ]
        if date:
            results = [
                *self.on_date(date, results)
            ]
        return results
    

class ScheduleDate(dict[str, FlightInstance]):
    def __contains__(self, key: str | FlightInstance):
        if isinstance(key, str):
            return super().__contains__(key)
        
        return key in self.values()
    
    def search(self, designator: str):  
        return [
            self[instance] for instance in
            search.basic(designator, self.keys())
        ]
    
    def route_search(self,
        origin: Airport,
        destination: Airport,
    ):
        return [
            instance for instance in self.values()
            if (instance.origin, instance.destination
            ) == (origin, destination)
        ]
    
    def add(self, instance: FlightInstance):
        self[instance.designator] = instance
        
    def remove(self, designator: str):
        del self[designator]


class ScheduleCatalog(dict[date, ScheduleDate]):
    @property
    def last_date(self):
        return max(self)
    
    @property
    def first_date(self):
        return min(self)
    
    def clear_history(self, _date: Optional[date] = None):
        """
        remove all schedules before the given date (today by default)
        """
        delta = (_date or date.today()) - self.first_date
        for day in daterange(delta.days - 1, self.first_date):
            self.remove(day)
                
    def add(self, date: date, schedule: ScheduleDate):        
        self[date] = schedule
    
    def remove(self, _date: date):
        del self[_date]
    
    
class FlightCatalog(list[Flight]):
    def search(self, designator: str):
        return search.simple(
            'designator', designator, self
        )
        
    def route_search(self,
        origin: Airport,
        destination: Airport,
    ):
        return [
            flight for flight in self
            if (flight.origin, flight.destination
            ) == (origin, destination)
        ]
        
    def add(self, flight: Flight):
        self.append(flight)
        
    def remove(self, flight: Flight):
        self.remove(flight)
    

class AirportCatalog(set[Airport]):
    def __contains__(self, key: str | Airport):
        if isinstance(key, Airport):
            return super().__contains__(key)
        
        for airport in self:
            if airport.location_code == key:
                return True
            
        return False
    
    def search(self, key: str):
        return [
            *search.multi_opt(
                'name', 'location_code', 'city', 'country',
                query=key, pool=self
            )
        ]
    
    # def load(self):
    #     with open('app/data/airport.csv') as f:
    #         data = ...
    #         for arg in data:
    #             self.add(Airport(*arg))


class AircraftCatalog(dict[str, Aircraft]):
    def __contains__(self, key: str | Aircraft):
        if isinstance(key, str):
            return super().__contains__(key)
        
        return key in self.values()
    
    def add(self, aricraft: Aircraft):
        self[aricraft.model] = aricraft
    
    def remove(self, aricraft: Aircraft):
        del self[aricraft.model]
    
    def search(self, model: str):
        return [
            self[aircraft] for aircraft in 
            search.basic(model, self.keys())
        ]
        
    # def load(self):
    #     with open('app/data/aircraft.csv') as f:
    #         data = ...
    #         for arg in data:
    #             self.add(Aircraft(*arg))
    
    
class AccountCatalog(dict[str, Account]):
    def __contains__(self, key: str | Account):
        if isinstance(key, str):
            if super().__contains__(key):
                return True
        
            return self.contains_email(key)
        
        elif isinstance(key, Account):
            if super().__contains__(key.username):
                return True
            
            return self.contains_email(key.email)
    
    # def __repr__(self):
    #     return '\n'.join(
    #         repr(account) for account in self.values()
    #     )
        
    def contains_email(self, email: str):
        for account in self.values():
            if account.email == email:
                return True
            
        return False
    
    def add(self, account: Account):
        self[account.username] = account
    
    def remove(self, account: Account):
        del self[account.username]
    
    def search(self, username: str):
        return [
            self[account] for account in 
            search.basic(username, self.keys())
        ]


if __name__ == '__main__':
    q = AccountCatalog()
    a = Account('admin', 'admin', 'admin', 'admin')
    q.add(a)
    x = 'admin' in q
