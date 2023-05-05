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

    def __iter__(self):
        yield from self.__plans
    
    @property
    def advance_days(self):
        return self.__advance_days
    
    def set_advance_days(self, days: int):
        self.__advance_days = days
    
    def add(self, plan: FlightPlan):
        designator = plan.flight.designator
        
        for some_plan in self:
            if some_plan.flight.designator == designator and some_plan in plan:
                raise KeyError(f'Flight {designator} already in {some_plan}')
                
        self.__plans.append(plan)
    
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
        

class ScheduleCatalog:
    def __init__(self):
        self.__schedules_date: list[ScheduleDate] = []

    def __iter__(self):
        yield from self.__schedules_date

    def add(self, schedules_date: ScheduleDate):
        self.__schedules_date.append(schedules_date)
    
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
                self.__schedules_date.remove(schedule)


class FlightCatalog:
    def __init__(self):
        self.__flights: list[Flight] = []

    def __iter__(self):
        yield from self.__flights

    def add(self, flight: Flight):
        self.__flights.append(flight)

    def extend(self, flights: Iterable[Flight]):
        self.__flights.extend(flights)
    
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


class AirportCatalog:
    def __init__(self):
        self.__airports: list[Airport] = []

    def __iter__(self):
        yield from self.__airports
    
    def __contains__(self, key: str | Airport):
        if isinstance(key, Airport):
            if self.__airports.__contains__(key):
                return True
            
            key = key.code
        try:
            self.get(key)
        except KeyError:
            return False
        else:
            return True

    @property
    def items(self):
        return self.__airports

    def add(self, airport: Airport):
        self.__airports.append(airport)
    
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


class AircraftCatalog:
    def __init__(self):
        self.__aircrafts: list[Aircraft] = []

    def __iter__(self):
        yield from self.__aircrafts
    
    def __contains__(self, key: str | Aircraft):
        if isinstance(key, Aircraft):
            if key in self.__aircrafts:
                return True
            
            key = key.model
        try:
            self.get(key)
        except KeyError:
            return False
        else:
            return True

    @property
    def items(self):
        return self.__aircrafts

    def add(self, aircraft: Aircraft):
        self.__aircrafts.append(aircraft)
    
    def search(self, model: str):
        results = search.simple('model', model, self)
        return list(results)
    
    def get(self, model: str):
        for aircraft in self:
            if aircraft.model == model:
                return aircraft
            
        raise KeyError


class AccountCatalog:
    def __init__(self):
        super().__init__()
        self.__accounts: list[Account] = []

    def __iter__(self):
        yield from self.__accounts
    
    def __contains__(self, key: str | Account):
        if isinstance(key, str):
            try:
                self.get(key)
            except KeyError:
                return False
            else:
                return True
                                
        elif isinstance(key, Account):
            if key in self.__accounts:
                return True
            
            for account in self:
                if account.username == key.username or account.email == key.email:
                    return True

        return False

    def add(self, account: Account):
        self.__accounts.append(account)
    
    def search(self, username: str):
        result = search.simple('username', username, self)
        return list(result)
    
    def get(self, key: str):
        for account in self:
            if key in (account.username, account.email):
                return account
            
        raise KeyError

    def get_customer(self, key: str):
        account = self.get(key)
        if not isinstance(account, Customer):
            raise KeyError
        
        return account