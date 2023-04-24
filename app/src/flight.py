from __future__ import annotations
from .base import *

from dataclasses import InitVar
if TYPE_CHECKING:
    from . import *


@dataclass(slots=True)
class Flight:
    """
    #### A flight template for FlightInstance, represent a flight
        - designator: `str`
            - aka "flight number" in colloquial term
    """
    __designator: str # type: ignore
    __departure: dt.time # type: ignore
    __arrival: dt.time # type: ignore
    __origin: Airport # type: ignore
    __destination: Airport # type: ignore
    
    @property
    def designator(self):
        return self.__designator
    
    @property
    def departure(self):
        return self.__departure
    
    @property
    def arrival(self):
        return self.__arrival
    
    @property
    def origin(self):
        return self.__origin
    
    @property
    def destination(self):
        return self.__destination


@dataclass(slots=True)
class FlightInstance:
    """
    A derivative from `Flight`, represent a process of flying 
    that will be operated on a specific date and aircraft
    
        - date: `datetime.date`
            - a date when this `FlightInstance` depart
        - flight: `Flight`
            - a template of this `FlightInstance`
        - aircraft: `Aircraft`
            - an aircraft that will be used for this `FlightInstance`
            
        - fares: `tuple[tuple[TravelClass, Fare], ...]`
            - a parameter for initializing components
            - represent a `Fare` for each travel class of this `FlightInstance`
            
        - components: `tuple[FlightClass, ...]`
            - a tuple of `FlightClass` which each represent a travel class section of this `FlightInstance`
    """
    __date: dt.date # type: ignore
    __flight: Flight # type: ignore
    __aircraft: Aircraft # type: ignore
    fares: InitVar[fares_param]
    
    __components: tuple[FlightClass, ...] = field(init=False)
    __status: FlightStatus = field(init=False, default=FlightStatus.SCHEDULED)
    
    def __post_init__(self, fares: fares_param):
        self.__components = tuple(
            FlightClass(self, travel_class, fare) 
            for travel_class, fare in fares
            if travel_class in self.all_travel_class
        )
    
    @property
    def flight(self):
        return self.__flight
    
    @property
    def date(self):
        return self.__date
    
    @property
    def aircraft(self):
        return self.__aircraft
    
    @property
    def status(self):
        return self.__status
    
    @property
    def departure(self):
        return dt.datetime.combine(self.date, self.flight.departure)
    
    @property
    def arrival(self):
        arrival_time = self.flight.arrival
        crossday = dt.timedelta(arrival_time < self.flight.departure)
        return dt.datetime.combine(self.date + crossday, arrival_time)
    
    @property
    def duration(self):
        return self.arrival - self.departure
    
    @property
    def all_travel_class(self):
        return {
            cabin.travel_class 
            for cabin in self.aircraft.all_cabins
        }
        
    def get_class(self, travel_class: TravelClass):
        for component in self.__components:
            if component.travel_class is travel_class:
                return component
            
        raise KeyError
        
    def transit_time(self, next: Self):
        return next.departure - self.arrival
        
    def cancel(self):
        self.__status = FlightStatus.CANCELLED
        
    def bookable(self, pax: Pax):
        """
        is any travel class in this flight bookable
        """
        return any(
            component.bookable(pax)
            for component in self.__components
        )
    

@dataclass(slots=True)
class FlightClass:
    """
        - One `FlightInstance` provides a service on different `TravelClass`, and each `TravelClass` is independent of each other.
        - Before customers book a flight they have to choose the `TravelClass` that was available, so they won't interfere with others `TravelClass`.
        - `FlightClass` represents the travel class service section of `FlighInstance`.
        - Most of the booking process involves with specific `TravelClass`. It is suitable to sperate `FlightClass` from `FlighInstance` and get them later by `TravelClass`.
            So we can use `FlightClass`'s methods directly instead of passing `TravelClass` to every `FlightInstance`'s methods.
    """
    __host: FlightInstance # type: ignore
    __travel_class: TravelClass # type: ignore
    __fare: Fare # type: ignore
    __booking_record: list[FlightReservation] = field(init=False, default_factory=list)
    
    @property
    def host(self):
        return self.__host
    
    @property
    def travel_class(self):
        return self.__travel_class
    
    @property
    def fare(self):
        return self.__fare
    
    @fare.setter
    def fare(self, value: Fare):
        """
            in case we want to update the price in this `Fare` which was shared with other flights (`FlightClass`), 
            but we want to change only for this flight
        """
        self.__fare = value
    
    @property
    def booking_record(self):
        return self.__booking_record
        
    def get_comfirmed(self):
        """
            get all confirmed reservations
        """
        for reservation in self.booking_record:
            if reservation.holder.status is BookingStatus.COMPLETED:
                yield reservation
        
    def get_occupied_seats(self):
        """
            get all reserved seats that have be paid (reservation status is confirmed)
        """
        return {
            selected.seat for reservation in self.get_comfirmed()
            for selected in reservation.selected if selected.seat
        }
        
    def get_remain_seats(self):
        """
            seats that have not been selected by any reservation
        """
        all = self.host.aircraft.get_seats_of(self.travel_class)
        occupied = self.get_occupied_seats()
        return all - occupied
    
    def get_seats_left(self):
        """
            not same as `get_occupied_seats`, it return as int which include a number of seats 
            that may not specified position in reservation
        """
        all_seats = self.host.aircraft.get_seats_of(self.travel_class)
        return len(all_seats) - sum(
            len(reservation.selected) for reservation in self.get_comfirmed()
        )
        
    def bookable(self, pax: Pax):
        return self.get_seats_left() >= pax.total

    def booked(self, reservation: FlightReservation):
        self.booking_record.append(reservation)
    
"""
ถ้าครอบครัวประกอบไปด้วยคนแต่ละคน
กลุ่มคนประกอบไปด้วยแต่ละครอบครัว
สหภาพที่ประกอบไปด้วยกลุ่มคน
สหพันธ์ประกอบไปด้วยสหภาพ

แต่ละการแบ่งนี้มีชุดการกระทำที่แตกต่างกัน 
ครอบครัวก็มีชุดการกระทำของครอบครัว
กลุ่มคนก็มีชุดการกระทำของกลุ่มคน
แต่กลุ่มคนและครอบครัวมีคุณลักษณะบางอย่างร่วมกันเช่น จำนวนคน
ดังนั้นในทุกชุดการแบ่งนี้ควรมี method จำนวนคน ของตนเอง?
"""