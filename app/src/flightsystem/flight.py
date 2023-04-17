from __future__ import annotations
from ..base import *

if TYPE_CHECKING:
    from app.src import FlightReservation, Aircraft, Airport, PassengerDetails, Seat, Pax


@dataclass(slots=True)
class Flight:
    """
    ### A flight template for FlightInstance
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
    
    @property
    def duration(self):
        return difference_time(self.departure, self.arrival)


@dataclass(slots=True, frozen=True)
class Fare:
    __travel_class: TravelClass # type: ignore
    __passenger_fare: list[tuple[PassengerType, int]] # type: ignore
    __seat_fare: list[tuple[SeatType, int]] # type: ignore

    @property
    def travel_class(self):
        return self.__travel_class
    
    def get_passenger_price(self, passenger_type: PassengerType):
        for type, price in self.__passenger_fare:
            if type is passenger_type:
                return price
        raise KeyError
    
    def set_passenger_price(self, passenger_type: PassengerType, price: int):
        for i, (type, _) in enumerate(self.__passenger_fare):
            if type is passenger_type:
                self.__passenger_fare[i] = (type, price)
                break
        else:
            self.__passenger_fare.append(
                (passenger_type, price)
            )

    def get_seat_price(self, seat_type: SeatType):
        for type, price in self.__seat_fare:
            if type is seat_type:
                return price
        raise KeyError
    
    def set_seat_price(self, seat_type: SeatType, price: int):
        for i, (type, _) in enumerate(self.__seat_fare):
            if type is seat_type:
                self.__seat_fare[i] = (type, price)
                break
        else:
            self.__seat_fare.append(
                (seat_type, price)
            )
            
    def get_price(self, 
        passenger_type: PassengerType, 
        seat_type: Optional[SeatType] = None
    ):
        """
        if seat_type is None, assume that passenger is not assigned a seat (can be any seat)
        so a fee for choosing a seat is not included
        """
        return sum([
            self.get_passenger_price(passenger_type), 
            self.get_seat_price(seat_type) if seat_type else 0
        ])


@dataclass(slots=True)
class FlightInstance:
    """
    ### A derivative of Flight
    """
    __date: dt.date # type: ignore
    __flight: Flight # type: ignore
    __aircraft: Aircraft # type: ignore
    __fares: tuple[Fare] # type: ignore
    
    __booking_record: list[FlightReservation] = field(init=False, default_factory=list)
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
        
    def get_fare(self, travel_class: TravelClass):
        for fare in self.__fares:
            if fare.travel_class == travel_class:
                return fare
        raise KeyError
        
    def cancel(self):
        self.__status = FlightStatus.CANCELLED
    
    def get_all_comfirmed(self):
        """
        get all confirmed reservations of this FlightInstance
        """
        return [
            reservation for reservation in self.booking_record
            if reservation.holder.status == BookingStatus.COMPLETED
        ]
    
    def get_occupied_of(self, travel_class: TravelClass):
        """
        get all reserved seats that have be paid (reservation status is confirmed)
        """
        return {
            seat for reservation in self.get_comfirmed_of(travel_class) if reservation.selected
            for selected in reservation.selected if (seat := selected.seat) is not None
        }
        
    def get_comfirmed_of(self, travel_class: TravelClass):
        """
        get confirmed reservations that match travel_class of this FlightInstance
        """
        return [
            reservation for reservation in self.get_all_comfirmed() 
            if reservation.travel_class == travel_class
        ]

    def bookable(self, pax: Pax, travel_class: TravelClass):
        """
        if specified travel class of this FlightInstance is bookable for pax (number of passenger)
        """
        seats_left = self.get_seats_left(travel_class)
        return len(seats_left) >= pax.total_capable
    
    def booked(self, reservation: FlightReservation):
        self.booking_record.append(reservation)
        
    def get_seats_left(self, travel_class: TravelClass):
        all = self.aircraft.get_seats_of(travel_class)
        occupied = self.get_occupied_of(travel_class)
        return all - occupied