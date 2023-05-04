r"""
https://fastapi.tiangolo.com/tutorial/body

not confuse with class in app\src,
these class is used for converting json to pydantic model 
and transforming src back to pydantic model, 
which done automatically by fastapi (read more in link above)
...
with these implementation, we can use pydantic model as a type hint and know specified attribute which can't done by raw dict
"""
from app.base import *

from pydantic import BaseModel
import app.src as src


travel_class_description: dict[TravelClass, list[str]] = {
    TravelClass.ECONOMY: [
        'economy',
    ],
    TravelClass.BUSSINESS: [
        'bussiness',
    ],
    TravelClass.FIRST: [
        'first',
    ],
}

seat_description: dict[SeatType, list[str]] = {
    SeatType.WINDOW: [
        'window',
    ],
    SeatType.AISLE: [
        'aisle',
    ],
    SeatType.LEGROOM: [
        'middle',
    ],
} #!


class AccountBody(BaseModel):
    username: str
    email: str
    phone: str
    status: AccountStatus = AccountStatus.INACTIVE
    
    @classmethod
    def transform(cls, obj: src.Customer):
        return cls(
            username=obj.username,
            email=obj.email,
            phone=obj.phone,
            status=obj.status,
        )
    
    def convert(self, password: str):
        return src.Customer(
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

    @classmethod
    def transforms(cls, objs: Sequence[src.Passenger]):
        return [
            cls.transform(passenger) for passenger in objs
        ]
        
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
            origin=flight.origin.code,
            destination=flight.destination.code,
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
                    info=travel_class_description[travel_class],
                 ) for travel_class in obj.all_travel_class
            ]
        )

    def get_class(self, travel_class: TravelClass):
        return next(
            classinfo for classinfo in self.classes
            if classinfo.travel_class == travel_class
        )


class FlightInstanceBody(BaseModel):
    """
        FlightInstance for converting from json
    """
    date: dt.date
    designator: str
    
    def convert(self):
        from app.__main__ import system
        
        schedule = system.schedules.get(self.date)
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
                for description in seat_description[subtype]
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
    decks: list[list[CabinBody]]
    
    @classmethod
    def transform(cls, obj: src.Aircraft):
        return cls(
            model=obj.model,
            decks=[
                CabinBody.transforms(deck) for deck in obj.decks
            ]
        )


class AirportBody(BaseModel):
    code: str
    name: str
    country: str
    
    @classmethod
    def transform(cls, obj: src.Airport):
        return cls(
            code=obj.code,
            name=obj.name,
            country=obj.country,
        )

     
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
    
    @classmethod
    def transform(cls, obj: Optional[src.Payment]):
        if obj is not None:
            return cls(
                transaction_id=obj.transaction_id,
                payment_time=obj.datetime,
                total_price=obj.total_price,
            )
    
    
class BookingBody(BaseModel):
    """
    shallow booking's data
    intent to use when user want to see preview of all bookings
    - `trip`: `tuple[origin, destination, departure, arrival]`
        - `
    """
    reference: UUID
    datetime: dt.datetime
    status: BookingStatus
    
    pax: list[tuple[PassengerType, int]]
    trip: list[
        tuple[AirportBody, AirportBody, dt.date, dt.date]
    ]
    
    @classmethod
    def transform(cls, obj: src.Booking):
        trip = []
        for flight in obj.reservations:
            first = flight[0].provider.host
            last = flight[-1].provider.host
            trip.append((
                AirportBody.transform(first.flight.origin),
                AirportBody.transform(last.flight.destination),
                first.date, last.date,
            ))
        return cls(
            reference=obj.reference,
            datetime=obj.datetime,
            status=obj.status,
            pax=list(obj.get_pax()),
            trip=trip
        )


class PreBookingBody(BaseModel):
    """
    temporary data that is needed for create booking
    """
    journey: list[tuple[list[FlightInstanceBody], TravelClass]]
    contact: ContactInfoBody
    passengers: list[PassengerBody]

    def convert(self):
        journey = [(
                FlightInstanceBody.converts(itinerary), travel_class
            ) for itinerary, travel_class in self.journey
        ]
        passengers = PassengerBody.converts(self.passengers)
        contact = self.contact.convert(passengers)
        return journey, contact, passengers


class BookingInfoBody(BaseModel):
    """
    deeper booking's data
    intent to use when user want to see specfic detail of one booking
    """
    reference: UUID
    datetime: dt.datetime
    status: BookingStatus
    
    price: int
    passengers: list[PassengerBody]
    contact: ContactInfoBody
    payment: Optional[PaymentBody]
    segments: list[list[FlightReservationBody]]
    
    @classmethod
    def transform(cls, obj: src.Booking):
        return cls(
            reference=obj.reference,
            datetime=obj.datetime,
            status=obj.status,
            price=obj.get_price(),
            payment=PaymentBody.transform(obj.payment),
            contact=ContactInfoBody.transform(obj.contact, obj.passengers),
            segments=FlightReservationBody.transforms(obj.reservations),
            passengers=PassengerBody.transforms(obj.passengers),
        )