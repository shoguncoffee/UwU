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
        return [
            *search.simple('designator', designator, self)
        ]
        
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
    
    def add(self, aircraft: Aircraft):
        self[aircraft.model] = aircraft
    
    def remove(self, aircraft: Aircraft):
        del self[aircraft.model]
    
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
    acc = AccountCatalog()
    acc1 = Account(
        'admin', 'admin', 
        'jinny@uwu.com', '0000'
    )
    acc2 = Account(
        'user', '123456', 
        'jame@uwu.com', '0000'
    )
    acc.add(acc1)
    
    port = AirportCatalog()
    port1 = Airport(
        'Don Mueang International Airport', 
        'DMK', 'Bangkok', 'Thailand'
    )
    port2 = Airport(
        'Cairo International Airport', 
        'CAI', 'Cairo', 'Egypt'
    )
    port.add(port1)
    
    
    from app.src import Desk
        
    craft = AircraftCatalog()
    craft1 = Aircraft(
        'Boeing 777', (
            Desk.generate(
                (TravelClass.BUSSINESS, [
                    (4, [2, 2, 2])
                ]),
                (TravelClass.BUSSINESS, [
                    (3, [2, 2, 2])
                ]),
                (TravelClass.ECONOMY, [
                    (2, [3, 3, 3]),
                    (8, [3, 4, 3]),
                    (1, [0, 4, 0])
                ]),
                (TravelClass.ECONOMY, [
                    (2, [3, 3, 3]),
                    (8, [3, 4, 3]),
                    (3, [3, 3, 3]),
                    (1, [2, 3, 2]),
                ])
            ),
        )
    )
    craft2 = Aircraft(
        'Airbus 320', (
            Desk.generate(
                (TravelClass.BUSSINESS, [
                    (4, [2, 2, 2])
                ]),
                (TravelClass.BUSSINESS, [
                    (3, [2, 2, 2])
                ]),
                (TravelClass.ECONOMY, [
                    (10, [3, 2, 3])
                ]),
                (TravelClass.ECONOMY, [
                    (10, [3, 2, 3])
                ])
            ),
        )
    )
    craft.add(craft1)
    
    flight = FlightCatalog()
    flight1 = Flight(
        'UWU294', 
        time(12, 30), time(13, 50), 
        port1, port2
    )
    flight2 = Flight(
        'UWU1648', 
        time(8, 20), time(10, 40), 
        port2, port1
    )
    flight.add(flight1)
    
    schedule = ScheduleCatalog()
    d1 = ScheduleDate()
    schedule.add(
        date(2023, 2, 1), d1
    )
    
    '''q = FlightScheduling(3)
    q1 = FlightPlan(
        flight1, 
        date(2022, 11, 1), date(2023, 6, 24),
        default_aircraft=craft1,
        default_fare=20_000
    )
    q1 = FlightPlan(
        flight2,
        date(2023, 2, 3), date(2023, 5, 6),
        default_aircraft=craft2,
        default_fare=30_000
    )
    q.add(q1)'''
