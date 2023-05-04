"""
Catalog
"""
from app.base import *

from app.utils import search
from . import *


class FlightScheduling(list[FlightPlan]):
    """
    #### A tools to manage and organize flight in advance
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
        from app.__main__ import system
        
        for date in daterange(self.advance_days):
            try:
                schedule = system.schedules.get(date)
            except KeyError:
                schedule = ScheduleDate(date)
                system.schedules.append(schedule)
            
            for plan in self.on_date(date, plans):
                schedule.append(
                    FlightInstance(date, 
                        plan.flight, 
                        plan.default_aircraft, 
                        deepcopy(plan.default_fares)
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
        date: dt.date, 
        plans: Optional[Sequence[FlightPlan]] = None
    ):
        for plan in plans or self:
            if date in plan:
                yield plan
    
    def search(self,
        date: Optional[dt.date] = None,
        flight: Optional[Flight] = None,
    ) -> list[FlightPlan]:
        """
        search for FlighPlan of what flight, on what date (all by default)
        """
        results = self
        if flight:
            results = [
                plan for plan in results
                if plan.flight is flight
            ]
        if date:
            results = list(
                self.on_date(date, results)
            )
        return results


class ScheduleDate(list[FlightInstance]):
    def __init__(self, date: dt.date):
        self.__date = date
    
    @property
    def date(self):
        return self.__date
    
    def __contains__(self, key: str | FlightInstance):
        if isinstance(key, str):
            key = key.upper()
            for instance in self:
                if instance.flight.designator == key:
                    return True
        
        elif isinstance(key, FlightInstance):
            if super().__contains__(key):
                return True
            
            for instance in self:
                if instance.flight.designator == key.flight.designator:
                    return True
        
        return False
    
    def search(self, designator: str):  
        return list(search.simple('designator', designator, self))
    
    def get(self, designator: str):
        designator = designator.upper()
        for instance in self:
            if instance.flight.designator == designator:
                return instance
            
        raise KeyError
    
    def route_search(self,
        origin: Airport,
        destination: Airport,
    ):
        return [
            instance for instance in self if 
            (instance.flight.origin, instance.flight.destination) == (origin, destination)
        ]
    
    def append(self, instance: FlightInstance):
        if instance.date == self.date and instance not in self:
            super().append(instance)
        

class ScheduleCatalog(list[ScheduleDate]):
    @property
    def first(self):
        return min(self, key=lambda schedule: schedule.date)
    
    @property
    def last(self):
        return max(self, key=lambda schedule: schedule.date)
    
    def get(self, date: dt.date):
        for schedule in self:
            if schedule.date == date:
                return schedule
            
        raise KeyError
    
    def clear_history(self, date: Optional[dt.date] = None):
        """
        remove all schedules before the given date (today by default)
        """
        delta = (date or dt.date.today()) - self.first.date
        for day in daterange(delta.days - 1, self.first.date):
            if schedule := self.get(day):
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
            key = key.upper()
            for airport in self:
                if airport.code == key:
                    return True

        elif isinstance(key, Airport):
            if super().__contains__(key):
                return True
            
            for airport in self:
                if airport.code == key.code:
                    return True
        
        return False
    
    def search(self, key: str):
        return list(
            search.multi_opt(
                *Airport.__annotations__.keys(),
                query=key, pool=self
            )
        )
        
    def get(self, key: str):
        key = key.upper()
        for airport in self:
            if airport.code == key:
                return airport
            
        raise KeyError
    
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
    
    
    def get(self, model: str):
        for aircraft in self:
            if aircraft.model == model:
                return aircraft
            
        raise KeyError
    
    # def load(self):
    #     with open('app/data/aircraft.csv') as f:
    #         data = ...
    #         for arg in data:
    #             self.add(Aircraft(*arg))
    
    
class AccountCatalog(list[Customer]):
    def __contains__(self, key: str | Customer):
        if isinstance(key, str):
            for account in self:
                if account.username == key or account.email == key:
                    return True
                                
        elif isinstance(key, Customer):
            if super().__contains__(key):
                return True
            
            for account in self:
                if account.username == key.username or account.email == key.email:
                    return True

        return False
    
    def search(self, username: str):
        return list(search.simple('username', username, self))
    
    def get(self, key: str):
        for account in self:
            if account.username == key:
                return account
            
        raise KeyError