r"""
https://fastapi.tiangolo.com/tutorial/body

not confuse with class in app\src,
these class is used for converting json to pydantic model 
and transforming src back to pydantic model, 
which done automatically by fastapi (read more in link above)
...
with these implementation, we can use pydantic model as a type hint and know specified attribute which can't done by raw dict
"""
from .base import *

from pydantic import BaseModel
from . import descriptions


class AccountBody(BaseModel):
    username: str
    email: str
    phone: str
    status: AccountStatus = AccountStatus.PENDING
    
    @classmethod
    def transform(cls, obj: src.Account):
        return cls(
            username=obj.username,
            email=obj.email,
            phone=obj.phone,
            status=obj.status,
        )
    
    def convert(self, password: str):
        return src.Account(
            self.username,
            password,
            self.email,
            self.phone,
        )


class PassengerBody(BaseModel):
    forename: str
    surname: str
    birthdate: dt.date
    nationality: str
    passport_id: str
    gender: GenderType
    type: PassengerType

    @property
    def name(self):
        return f"{self.forename} {self.surname}"
    
    @classmethod
    def transform(cls, obj: src.Passenger):
        return cls(
            forename=obj.forename,
            surname=obj.surname,
            birthdate=obj.birthdate,
            nationality=obj.nationality,
            passport_id=obj.passport_id,
            gender=obj.gender,
            type=obj.type,
        )    
        
    def convert(self):
        return src.Passenger(*vars(self).values())
    
    @classmethod
    def converts(cls, objs: Sequence[Self]):
        return [
            obj.convert() for obj in objs
        ]


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
    
    @classmethod
    def transform(cls, obj: src.FlightInstance):
        flight = obj.flight
        return cls(
            designator=flight.designator,
            origin=flight.origin.location_code,
            destination=flight.destination.location_code,
            departure=flight.departure,
            arrival=flight.arrival,
            date=obj.date,
            aircraft_model=obj.aircraft.model,
        )

    def reduce(self):
        return FlightInstanceBody(
            date=self.date,
            designator=self.designator,
        )


class ClassInfoBody(BaseModel):
    travel_class: TravelClass
    seat_left: int
    price: int
    info: list[str]


class ItineraryBody(BaseModel):
    flights: list[FlightInfoBody]
    classes: list[ClassInfoBody]
    
    @classmethod
    def transform(cls, obj: src.FlightItinerary, pax: src.Pax):
        return cls(
            flights=[
                FlightInfoBody.transform(instance) for instance in obj
            ],
            classes=[
                ClassInfoBody(
                    travel_class=travel_class,
                    seat_left=obj.get_seats_left(travel_class),
                    price=obj.get_price(pax, travel_class),
                    info=descriptions.travel_class[travel_class],
                 ) for travel_class in obj.all_travel_class
            ]
        )


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
    def converts(cls, objs: Sequence[Self]):
        return src.FlightItinerary(
            obj.convert() for obj in objs
        )


class ContactInfoBody(BaseModel):
    index: int
    phone: str
    email: str
    
    @classmethod
    def transform(cls, 
        obj: src.ContactInformation, 
        passengers: Sequence[src.Passenger]
    ):
        return cls(
            index=passengers.index(obj.passenger),
            phone=obj.phone, 
            email=obj.email,
        )
        
    def convert(self, passengers: Sequence[src.Passenger]):
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
    
    @classmethod
    def transform(cls, obj: src.Seat):
        return cls(
            row=obj.row, 
            column=obj.column,
            number=obj.number,
            type=obj.type,
            descriptions=[
                description for subtype in obj.type
                for description in descriptions.seat[subtype]
            ]
        )
            
    @classmethod
    def transforms(cls, 
        selected: Sequence[src.SeatReservation]
    ):
        return [
            cls.transform(select.seat) if select.seat else None 
            for select in selected
        ]
     
     
class FlightReservationBody(BaseModel):
    travel_class: TravelClass
    selected: list[SeatBody | None]
    is_assigned: bool
    flight: FlightInfoBody
    
    @classmethod
    def transform(cls, obj: src.FlightReservation):
        return cls(
            travel_class=obj.provider.travel_class,
            selected=SeatBody.transforms(obj.selected),
            is_assigned=obj.is_assigned,
            flight=FlightInfoBody.transform(obj.provider.host),
        )
    
    @classmethod
    def transforms(cls, journey: Sequence[Sequence[src.FlightReservation]]):
        return [
            [cls.transform(obj) for obj in segment] for segment in journey
        ]


class PaymentBody(BaseModel):
    transaction_id: UUID
    payment_time: dt.datetime
    total_price: int
    status: PaymentStatus
    
    @classmethod
    def transform(cls, obj: src.Payment):
        return cls(
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
    
    @classmethod
    def transform(cls, obj: src.Booking):
        return cls(
            datetime=obj.datetime,
            reference=obj.reference,
            status=obj.status,
            payment=PaymentBody.transform(obj.payment) if obj.payment else None,
            contact=ContactInfoBody.transform(obj.contact, obj.passengers),
            segments=FlightReservationBody.transforms(obj.reservations),
            passengers=[
                PassengerBody.transform(passenger) for passenger in obj.passengers
            ],
        )
    
    
class PaxBody(BaseModel):
    pax: list[tuple[PassengerType, int]]
    
    def convert(self):
        return src.Pax(self.pax)
    
    
class CabinBody(BaseModel):
    travel_class: TravelClass
    seats: list[SeatBody]
    
    @classmethod
    def transform(cls, obj: src.Cabin):
        return cls(
            travel_class=obj.travel_class,
            seats=[
                SeatBody.transform(seat) for seat in obj.seats
            ],
        )
    
    @classmethod
    def transforms(cls, objs: Sequence[src.Cabin]):
        return [
            cls.transform(cabin) for cabin in objs
        ]
        
    
class AircraftBody(BaseModel):
    model: str
    desks: list[list[CabinBody]]
    
    @classmethod
    def transform(cls, obj: src.Aircraft):
        return cls(
            model=obj.model,
            desks=[
                CabinBody.transforms(desk) for desk in obj.desks
            ]
        )


class AirportBody(BaseModel):
    location_code: str
    name: str
    country: str
    
    @classmethod
    def transform(cls, obj: src.Airport):
        return cls(
            location_code=obj.location_code,
            name=obj.name,
            country=obj.country,
        )