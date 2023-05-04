from app.base import *
from app.utils import search
from . import *


class FlightScheduling:
    """
        A tools to manage and organize flight in advance
    """
    def __init__(self, advance_days: int = 150):
        self.__plans: list[FlightPlan] = []
        self.set_advance_days(advance_days)
    
    @property
    def advance_days(self):
        return self.__advance_days
    
    def set_advance_days(self, days: int):
        self.__advance_days = days
    
    def add(self, plan: FlightPlan):
        designator = plan.flight.designator
        
        for some_plan in self.__plans:
            if some_plan.flight.designator == designator and some_plan in plan:
                raise KeyError(f'Flight {designator} already in {some_plan}')
                
        self.__plans.append(plan)
    
    def on_date(self, 
        date: dt.date, 
        plans: Optional[Sequence[FlightPlan]] = None
    ):
        for plan in plans or self.__plans:
            if date in plan:
                yield plan
    
    def search(self,
        date: Optional[dt.date] = None,
        flight: Optional[Flight] = None,
    ) -> list[FlightPlan]:
        """
            search for FlighPlan of what flight, on what date (all by default)
        """
        results = self.__plans
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


class ScheduleDate:
    def __init__(self, date: dt.date):
        self.__flight_instances: list[FlightInstance] = []
        self.__date = date

    def __iter__(self):
        yield from self.__flight_instances
    
    def __contains__(self, key: str | FlightInstance):
        if isinstance(key, FlightInstance):
            if key in self.__flight_instances:
                return True
            
            key = key.flight.designator
        try:
            self.get(key)
        except KeyError:
            return False
        else:
            return True
    
    @property
    def date(self):
        return self.__date
     
    def search(self, designator: str): 
        result = search.simple('designator', designator, self)
        return list(result)
    
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
    
    def add(self, instance: FlightInstance):
        if instance.date == self.date and instance not in self:
            self.__flight_instances.append(instance)
        

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
        first_date = self.first.date
        delta = (date or dt.date.today()) - first_date
        
        for day in daterange(delta.days - 1, first_date):
            if schedule := self.get(day):
                self.remove(schedule)


class FlightCatalog(list[Flight]):
    def search(self, designator: str):
        results = search.simple('designator', designator, self)
        return list(results)
        
    def route_search(self,
        origin: Airport,
        destination: Airport,
    ):
        return [
            flight for flight in self
            if (flight.origin, flight.destination) == (origin, destination)
        ]


class AirportCatalog(list[Airport]):
    def __contains__(self, key: str | Airport):
        if isinstance(key, Airport):
            if super().__contains__(key):
                return True
            
            key = key.code
        try:
            self.get(key)
        except KeyError:
            return False
        else:
            return True
    
    def search(self, key: str):
        results = search.multi_opt(
            *Airport.__annotations__.keys(),
            query=key, pool=self
        )
        return list(results)
        
    def get(self, key: str):
        key = key.upper()
        
        for airport in self:
            if airport.code == key:
                return airport
            
        raise KeyError


class AircraftCatalog(list[Aircraft]):
    def __contains__(self, key: str | Aircraft):
        if isinstance(key, Aircraft):
            if super().__contains__(key):
                return True
            
            key = key.model
        try:
            self.get(key)
        except KeyError:
            return False
        else:
            return True
    
    def search(self, model: str):
        results = search.simple('model', model, self)
        return list(results)
    
    def get(self, model: str):
        for aircraft in self:
            if aircraft.model == model:
                return aircraft
            
        raise KeyError


class AccountCatalog(list[Customer]):
    def __contains__(self, key: str | Customer):
        if isinstance(key, str):
            try:
                self.get(key)
            except KeyError:
                return False
            else:
                return True
                                
        elif isinstance(key, Customer):
            if super().__contains__(key):
                return True
            
            for account in self:
                if account.username == key.username or account.email == key.email:
                    return True

        return False
    
    def search(self, username: str):
        result = search.simple('username', username, self)
        return list(result)
    
    def get(self, key: str):
        for account in self:
            if key in (account.username, account.email):
                return account
            
        raise KeyError