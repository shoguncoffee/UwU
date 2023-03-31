"""
catalog
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from app.src import (
    Account,
    Customer,
    Trip,
    PassengerDetails,
    ContactInformation,
    FlightReservation,
    Aircraft,
    Airport,
    ScheduleDate,
    Flight,
    FlightPlan
)
class FlightScheduling:
    _instance: FlightScheduling 
    
    def __init__(self, advance_days: int = 365):
        self.__advance_days = advance_days
        self.__plans: list[FlightPlan] = []
    
    @property
    def advance_days(self):
        return self.__advance_days
    
    @property
    def plans(self):
        return self.__plans
    
    @classmethod
    def add(cls, plan: FlightPlan):
        cls._instance.__plans.append(plan)

class FlightScheduling(set[ScheduleDate]):
    def search():
        ...

class ScheduleCatalog :
    def __init__(self) :
        self.__records = []
    
    def add_new_date(self,schedule_date) :
        self.__records.append(schedule_date)
    def delete_history(self) :
        pass
    def search_flight(self,date,origin,destination,pax) :
        pass
    def get_possible_schedule_date(self,date) :
        for i in self.__records :
            pass
    def match_flight_itinerary_between_airport(self) :
        pass
    def create_flight_instance(self,date,flight,aircraft,base_price) :
        pass
    def get_flight_instance(self,origin,destination) :
        pass
    def modify_flight_instance(self,aircraft,base_price,flight_instance) :
        pass

    
class FlightCatalog(set[Flight]):
    def search():
        ...
    
class AirportCatalog(set[Airport]):
    def search():
        ...

    
class AircraftCatalog(set[Aircraft]):
    def search():
        ...

    
class AccountCatalog(set[Account]):
    def search():
        ...


if __name__ == '__main__':
    x = FlightScheduling()
    FlightCatalog()
    AirportCatalog()
    AircraftCatalog()
    AccountCatalog()