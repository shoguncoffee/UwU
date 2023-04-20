"""
https://fastapi.tiangolo.com/tutorial/body
"""
from telnetlib import STATUS

from .base import *
from pydantic import BaseModel


class AccountBody(BaseModel):
    username: str
    email: str
    phone: str
    status: AccountStatus
    
    @classmethod
    def transform(cls, obj: src.Account):
        return cls(
            username=obj.username,
            email=obj.email,
            phone=obj.phone,
            status=obj.status,
        )


class PassengerBody(BaseModel):
    forename: str
    surname: str
    birthdate: dt.date
    nationality: str
    passport_id: str
    gender: GenderType
    type: PassengerType
    
    def convert(self):
        return src.PassengerDetails(*vars(self).values())
    
    @classmethod
    def converts(cls, objs: Sequence[Self]):
        return [
            obj.convert() for obj in objs
        ]
    
    @classmethod
    def transform(cls, obj: src.PassengerDetails):
        return cls(
            forename=obj.forename,
            surname=obj.surname,
            birthdate=obj.birthdate,
            nationality=obj.nationality,
            passport_id=obj.passport_id,
            gender=obj.gender,
            type=obj.type,
        )
    
    @classmethod
    def transforms(cls, objs: Sequence[src.PassengerDetails]):
        return [
            cls.transform(obj) for obj in objs
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
journey = [
    (
        [{'date': '', 'designator': ''}, {'date': '', 'designator': ''}], 
        TravelClass.ECONOMY
    ),
]

class ClassBody(BaseModel):
    travel_class: TravelClass
    seat_left: int
    fare: int
    info: tuple[str, ...]
    
    @classmethod
    def init(cls, obj: src.FlightInstance, pax: src.Pax):
        return [
            cls(
                travel_class=travel_class,
                seat_left=len(obj.get_seats_left(travel_class)),
                fare=obj.get_fare(travel_class).pax_price(pax),
                info=travel_class_info[travel_class]
            ) for travel_class in obj.all_travel_class
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
    def transform(cls, obj: src.FlightInstance, pax: src.Pax):
        return cls(
            designator=obj.designator,
            origin=obj.origin.location_code,
            destination=obj.destination.location_code,
            departure=obj.flight.departure,
            arrival=obj.flight.arrival,
            date=obj.date,
            aircraft_model=obj.aircraft.model,
        )
    
    @classmethod
    def transforms(cls, objs: Sequence[src.FlightInstance], pax: src.Pax):
        return [{
            'flights': cls.transform(obj, pax),
            'class_of_travel': ClassBody.init(obj, pax)
            } for obj in objs
        ]
    
    
class ContactInfoBody(BaseModel):
    index: int
    phone: str
    email: str
    
    def convert(self, passengers: Sequence[src.PassengerDetails]):
        return src.ContactInformation(
            passengers[self.index], 
            self.phone, self.email,
        )
        
    @classmethod
    def transform(cls, 
        obj: src.ContactInformation, 
        passengers: Sequence[src.PassengerDetails]
    ):
        return cls(
            index=passengers.index(obj.passenger),
            phone=obj.phone, email=obj.email,
        )
     
     
class SeatBody(BaseModel):
    row: int
    column: int
    letter: str
    type: SeatType
    description: list[str]
    
    @classmethod
    def transform(cls, obj: src.Seat | None):
        if obj:
            return cls(
                row=obj.row, 
                column=obj.column,
                letter=obj.letter,
                type=obj.type,
                description=obj.description,
            )
            
    @classmethod
    def reservation_transforms(cls, 
        reservations: Sequence[src.SeatReservation] | None
    ):
        if reservations:
            return [
                cls.transform(reservation.seat) 
                for reservation in reservations
            ]
     
    @classmethod
    def transforms(cls, objs: Iterable[src.Seat]) -> list[Self]:
        return [
            cls.transform(obj) for obj in objs # type: ignore
        ]


class FlightReservationBody(BaseModel):
    travel_class: TravelClass
    selected: Optional[list[SeatBody | None]] # optional?
    flight: FlightInfoBody
    
    @classmethod
    def transform(cls, obj: src.FlightReservation, pax: src.Pax):
        return cls(
            travel_class=obj.travel_class,
            selected=SeatBody.reservation_transforms(obj.selected),
            flight=FlightInfoBody.transform(obj.flight, pax),
        )
        
    @classmethod
    def transforms(cls, objs: Sequence[src.FlightReservation], pax: src.Pax):
        return [
            cls.transform(obj, pax) for obj in objs
        ]


class PaymentBody(BaseModel):
    transaction_id: UUID
    payment_time: dt.datetime
    total_price: int
    status: PaymentStatus
    
    @classmethod
    def transform(cls, obj: src.Payment | None):
        if obj:
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
    reservations: list[FlightReservationBody]
        
    @classmethod
    def transform(cls, obj: src.Booking):
        return cls(
            datetime=obj.datetime,
            reference=obj.reference,
            status=obj.status,
            payment=PaymentBody.transform(obj.payment),
            contact=ContactInfoBody.transform(obj.contactinfo, obj.passengers),
            passengers=PassengerBody.transforms(obj.passengers),
            reservations=FlightReservationBody.transforms(obj.reservations, obj.pax),
        )
        
        
class PaxBody(BaseModel):
    pax: list[tuple[PassengerType, int]]
    
    def convert(self):
        return src.Pax(self.pax)
    
    
class CabinBody(BaseModel):
    travel_class: TravelClass
    seats: list[SeatBody]
    
    @classmethod
    def transform(cls, desk: src.Desk):
        return [
            cls(
                travel_class=cabin.travel_class,
                seats=SeatBody.transforms(cabin.seats)
            ) for cabin in desk.cabins
        ]
        
    @classmethod
    def transforms(cls, desks: Sequence[src.Desk]):
        return [
            cls.transform(desk) for desk in desks
        ]
    
    
class AircraftBody(BaseModel):
    model: str
    desks: list[list[CabinBody]]
    
    @classmethod
    def transform(cls, obj: src.Aircraft):
        return cls(
            model=obj.model,
            desks=CabinBody.transforms(obj.desks)
        )
      
        
class AirportBody(BaseModel):
    location_code: str
    name: str
    city: str
    country: str
    
    @classmethod
    def transform(cls, obj: src.Airport):
        return cls(
            location_code=obj.location_code,
            name=obj.name,
            city=obj.city,
            country=obj.country,
        )
        
    @classmethod
    def transforms(cls, objs: Sequence[src.Airport]):
        return [
            cls.transform(obj) for obj in objs
        ]