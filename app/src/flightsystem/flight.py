from __future__ import annotations
from ..base import *

if TYPE_CHECKING:
    from app.src import *     


@dataclass(slots=True)
class Flight:
    """
    A flight template for FlightInstance
    """
    __designator: str # type: ignore
    __departure: time # type: ignore
    __arrival: time # type: ignore
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
    
    @property
    def duration(self) -> timedelta:
        crossday = timedelta(self.arrival < self.departure)
        d2 = datetime.combine(date.min + crossday, self.arrival)
        d1 = datetime.combine(date.min, self.departure)
        return d2 - d1


@dataclass(slots=True)
class FlightInstance:
    """
    A derivative of Flight
    """
    __date: date # type: ignore
    __flight: Flight # type: ignore
    __aircraft: Aircraft # type: ignore
    
    __base_fare: float # type: ignore
    
    __booking_record: set[FlightReservation] = field(init=False, default_factory=set)
    __status: FlightStatus = field(init=False, default=FlightStatus.SCHEDULED)
    
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
    def booking_record(self):
        return self.__booking_record
    
    @property
    def status(self):
        return self.__status
    
    @property
    def base_fare(self):
        return self.__base_fare
    
    @property
    def designator(self):
        return self.flight.designator
    
    @property
    def origin(self):
        return self.flight.origin
    
    @property
    def destination(self):
        return self.flight.destination
    
    @property
    def all_travel_class(self):
        return {
            cabin.travel_class for desk in self.aircraft.desks 
            for cabin in desk.cabins
        }
    
    def cancel(self):
        self.__status = FlightStatus.CANCELLED
    
    def get_seats_of(self, travel_class: TravelClass):
        return self.aircraft.get_seats_of(travel_class)
    
    def get_all_comfirmed(self):
        """
        get all confirmed reservations of this FlightInstance
        """
        return {
            reservation for reservation in self.booking_record 
            if reservation.holder.status == BookingStatus.COMPLETED
        }
    
    def get_occupied_of(self, travel_class: TravelClass):
        """
        get all reserved seats that have be paid (reservation status is confirmed)
        """
        return {
            seatRE.seat for flightRE in self.get_comfirmed_of(travel_class)
            for seatRE in flightRE.reservation
        }
        
    def get_comfirmed_of(self, travel_class: TravelClass):
        """
        get confirmed reservations that match travel_class of this FlightInstance
        """
        return {
            reservation for reservation in self.get_all_comfirmed() 
            if reservation.travel_class == travel_class
        }

    def bookable(self, travel_class: TravelClass, pax: int):
        """
        if specified travel class of this FlightInstance is bookable for pax
        """
        free = self.get_seats_of(travel_class)
        occupied = self.get_occupied_of(travel_class)
        return len(free) - len(occupied) >= pax
    
    def bookingable(self, pax: int):
        """
        if any travel class of this FlightInstance bookable for pax
        """
        return any(
            self.bookable(travel_class, pax) 
            for travel_class in self.all_travel_class
        )
    
    def booked(self, reservation: FlightReservation):
        self.booking_record.add(reservation)