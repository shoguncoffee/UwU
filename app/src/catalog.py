"""
Catalog
"""
from __future__ import annotations
from .base import *

from app.utils import search
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
    
    def update(self, *plans: FlightPlan):
        from app.system import Airline
        
        for date in daterange(self.advance_days):
            schedule = Airline.schedules.search(date)
            if schedule is None:
                schedule = ScheduleDate(date)
                Airline.schedules.append(schedule)
            
            for plan in self.on_date(date, plans):
                schedule.append(
                    FlightInstance(date, 
                        plan.flight, 
                        plan.default_aircraft, 
                        plan.default_fare
                    )
                )
    
    def append(self, plan: FlightPlan):
        for p in self:
            if p.flight.designator == plan.flight.designator:
                if p in plan: break
        else:
            super().append(plan) 
            self.update(plan)
    
    def on_date(self, 
        date: date, 
        plans: Optional[Sequence[FlightPlan]] = None
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
            results = list(
                self.on_date(date, results)
            )
        return results


class ScheduleDate(list[FlightInstance]):
    def __init__(self, date: date):
        self.__date = date
    
    @property
    def date(self):
        return self.__date
    
    def __contains__(self, key: str | FlightInstance):
        if isinstance(key, str):
            for instance in self:
                if instance.designator == key:
                    return True
        
        elif isinstance(key, FlightInstance):
            if super().__contains__(key):
                return True
            
            for instance in self:
                if instance.designator == key.designator:
                    return True
        
        return False
    
    def search(self, designator: str):  
        return list(search.simple('designator', designator, self))
    
    def route_search(self,
        origin: Airport,
        destination: Airport,
    ):
        return [
            instance for instance in self
            if (instance.origin, instance.destination
            ) == (origin, destination)
        ]
    
    def append(self, instance: FlightInstance):
        if instance.date == self.date:
            super().append(instance)
        

class ScheduleCatalog(list[ScheduleDate]):
    @property
    def first(self):
        return min(self, key=lambda schedule: schedule.date)
    
    @property
    def last(self):
        return max(self, key=lambda schedule: schedule.date)
    
    def search(self, date: date):
        for schedule in self:
            if schedule.date == date:
                return schedule
    
    def clear_history(self, _date: Optional[date] = None):
        """
        remove all schedules before the given date (today by default)
        """
        delta = (_date or date.today()) - self.first.date
        for day in daterange(delta.days - 1, self.first.date):
            if schedule := self.search(day):
                self.remove(schedule)


class FlightCatalog(list[Flight]):
    def search(self, designator: str):
        return list(search.simple('designator', designator, self))
        
    def route_search(self,
        origin: Airport,
        destination: Airport,
    ):
        return [
            flight for flight in self
            if (flight.origin, flight.destination
            ) == (origin, destination)
        ]


class AirportCatalog(list[Airport]):
    def __contains__(self, key: str | Airport):
        if isinstance(key, str):
            for airport in self:
                if airport.location_code == key:
                    return True

        elif isinstance(key, Airport):
            if super().__contains__(key):
                return True
            
            for airport in self:
                if airport.location_code == key.location_code:
                    return True
        
        return False
    
    def search(self, key: str):
        return list(
            search.multi_opt(
                'name', 'location_code', 'city', 'country',
                query=key, pool=self
            )
        )
    
    # def load(self):
    #     with open('app/data/airport.csv') as f:
    #         data = ...
    #         for arg in data:
    #             self.add(Airport(*arg))


class AircraftCatalog(list[Aircraft]):
    def __contains__(self, key: str | Aircraft):
        if isinstance(key, str):
            for aircraft in self:
                if aircraft.model == key:
                    return True
                        
        elif isinstance(key, Aircraft):
            if super().__contains__(key):
                return True
            
            for account in self:
                if account.model == key.model:
                    return True
        
        return False
    
    def search(self, model: str):
        return list(search.simple('model', model, self))
        
    # def load(self):
    #     with open('app/data/aircraft.csv') as f:
    #         data = ...
    #         for arg in data:
    #             self.add(Aircraft(*arg))
    
    
class AccountCatalog(list[Account]):
    def __contains__(self, key: str | Account):
        if isinstance(key, str):
            for account in self:
                if account.username == key or account.email == key:
                    return True
                                
        elif isinstance(key, Account):
            if super().__contains__(key):
                return True
            
            for account in self:
                if account.username == key.username or account.email == key.email:
                    return True
                
        return False
            
    
    # def __repr__(self):
    #     return '\n'.join(
    #         repr(account) for account in self.values()
    #     )
    def search(self, username: str):
        return list(search.simple('username', username, self))