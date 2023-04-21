r"""
https://fastapi.tiangolo.com/tutorial/body

not confuse with class in app\src,
these class is used for converting json to pydantic model 
and transforming back src to pydantic model, 
which done automatically by fastapi (read more in link above)
...
with these implementation, we can use pydantic model as a type hint and know specified attribute which can't done by raw dict
"""

from .base import *
from pydantic import BaseModel


class AccountBody(BaseModel):
    username: str
    email: str
    phone: str
    status: AccountStatus
    
    def __init__(self, obj: src.Account):
        super().__init__(
            username=obj.username,
            email=obj.email,
            phone=obj.phone,
            status=obj.status,
        )
    
    def convert(cls, password: str):
        return src.Account(
            cls.username,
            password,
            cls.email,
            cls.phone,
        )


class PassengerBody(BaseModel):
    forename: str
    surname: str
    birthdate: dt.date
    nationality: str
    passport_id: str
    gender: GenderType
    type: PassengerType
    
    def __init__(self, obj: src.PassengerDetails):
        super().__init__(
            forename=obj.forename,
            surname=obj.surname,
            birthdate=obj.birthdate,
            nationality=obj.nationality,
            passport_id=obj.passport_id,
            gender=obj.gender,
            type=obj.type,
        )    
        
    def convert(self):
        return src.PassengerDetails(*vars(self).values())
    
    @classmethod
    def converts(cls, objs: Sequence[Self]):
        return [
            obj.convert() for obj in objs
        ]
    

class FlightInstanceBody(BaseModel):
    """
    FlightInstance for converting from json
    """
    date: dt.date
    designator: str
    
    def convert(self):
        schedule = Airline.schedules.get(self.date)
        return schedule.get(self.designator)
    
    @classmethod
    def converts(self, objs: Sequence[Self]):
        return src.FlightItinerary(
            obj.convert() for obj in objs
        )


travel_class_info: dict[TravelClass, tuple[str, ...]] = {
    TravelClass.ECONOMY: (
        'economy',
    ),
    TravelClass.BUSSINESS: (
        'bussiness',
    ),
    TravelClass.FIRST: (
        'first',
    ),
}
class FlightInfoBody(BaseModel):
    """
    Flightinstance for transform to json
    """
    designator: str
    origin: str
    destination: str
    departure: dt.time
    arrival: dt.time
    date: dt.date
    aircraft_model: str
    
    def __init__(self, obj: src.FlightInstance):
        flight = obj.flight
        super().__init__(
            designator=obj.designator,
            origin=flight.origin.location_code,
            destination=flight.destination.location_code,
            departure=flight.departure,
            arrival=flight.arrival,
            date=obj.date,
            aircraft_model=obj.aircraft.model,
        )
    
    @classmethod
    def transforms(cls, objs: src.FlightItinerary, pax: src.Pax):
        return {
            'flights': [
                cls(obj) for obj in objs
            ],
            'classes': {
                'travel_class': {
                    'seat_left': objs.get_seats_left(travel_class),
                    'price': objs.get_price(pax, travel_class),
                    'info': travel_class_info[travel_class],
                } for travel_class in objs.all_travel_class
            }
        }
    
    
class ContactInfoBody(BaseModel):
    index: int
    phone: str
    email: str
    
    def __init__(self, 
        obj: src.ContactInformation, 
        passengers: Sequence[src.PassengerDetails]
    ):
        super().__init__(
            index=passengers.index(obj.passenger),
            phone=obj.phone, 
            email=obj.email,
        )   
    
    def convert(self, passengers: Sequence[src.PassengerDetails]):
        return src.ContactInformation(
            passengers[self.index], 
            self.phone, 
            self.email,
        )
     
     
class SeatBody(BaseModel):
    row: int
    column: int
    number: str
    type: SeatType
    descriptions: list[str]
    
    def __init__(self, obj: src.Seat):
        super().__init__(
            row=obj.row, 
            column=obj.column,
            number=obj.number,
            type=obj.type,
            descriptions=obj.descriptions,
        )
            
    @classmethod
    def transforms(cls, 
        selected: Sequence[src.SeatReservation]
    ):
        return [
            cls(select.seat) if select.seat else None 
            for select in selected
        ]
     
     
class FlightReservationBody(BaseModel):
    travel_class: TravelClass
    selected: list[SeatBody | None]
    is_assigned: bool
    flight: FlightInfoBody
    
    def __init__(self, obj: src.FlightReservation):
        super().__init__(
            travel_class=obj.provider.travel_class,
            selected=SeatBody.transforms(obj.selected),
            is_assigned=obj.is_assigned,
            flight=FlightInfoBody(obj.provider.host),
        )
        
    @classmethod
    def transforms(cls, journey: Sequence[Sequence[src.FlightReservation]]):
        return [
            [cls(obj) for obj in segment] for segment in journey
        ]


class PaymentBody(BaseModel):
    transaction_id: UUID
    payment_time: dt.datetime
    total_price: int
    status: PaymentStatus
    
    
    def __init__(cls, obj: src.Payment):
        super().__init__(
            transaction_id=obj.transaction_id,
            payment_time=obj.datetime,
            total_price=obj.total_price,
            status=obj.status,
        )
    
    
class BookingBody(BaseModel):
    datetime: dt.datetime
    reference: UUID
    status: BookingStatus
    payment: Optional[PaymentBody]
    contact: ContactInfoBody
    passengers: list[PassengerBody]
    segments: list[list[FlightReservationBody]]
        
    def __init__(self, obj: src.Booking):
        super().__init__(
            datetime=obj.datetime,
            reference=obj.reference,
            status=obj.status,
            payment=PaymentBody(obj.payment) if obj.payment else None,
            contact=ContactInfoBody(obj.contact, obj.passengers),
            segments=FlightReservationBody.transforms(obj.reservations),
            passengers=[
                PassengerBody(passenger) for passenger in obj.passengers
            ],
        )
    
    
class PaxBody(BaseModel):
    pax: list[tuple[PassengerType, int]]
    
    def convert(self):
        return src.Pax(self.pax)
    
    
class CabinBody(BaseModel):
    travel_class: TravelClass
    seats: list[SeatBody]
    
    def __init__(self, obj: src.Cabin):
        super().__init__(
            travel_class=obj.travel_class,
            seats=obj.seats,
        )
    
    @classmethod
    def transforms(cls, objs: Sequence[src.Cabin]):
        return [
            cls(cabin) for cabin in objs
        ]
        
    
    
class AircraftBody(BaseModel):
    model: str
    desks: list[list[CabinBody]]
    
    def __init__(self, obj: src.Aircraft):
        super().__init__(
            model=obj.model,
            desks=[
                CabinBody.transforms(desk) for desk in obj.desks
            ]
        )
      
        
class AirportBody(BaseModel):
    location_code: str
    name: str
    city: str
    country: str
    
    def __init__(self, obj: src.Airport):
        super().__init__(
            location_code=obj.location_code,
            name=obj.name,
            city=obj.city,
            country=obj.country,
        )