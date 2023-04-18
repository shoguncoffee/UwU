from __future__ import annotations
from ..base import *

if TYPE_CHECKING:
    from app.src import Booking

@dataclass(slots=True)
class Account:
    _username: str
    _password: str
    _email: str
    _phone: str
    _status: AccountStatus = field(init=False, default=AccountStatus.PENDING)
    # __reference: str = field(init=False)
    
    @property
    def username(self):
        return self._username
    
    @property
    def email(self):
        return self._email
    
    @property
    def phone(self):
        return self._phone
    
    @property
    def status(self):
        return self._status


@dataclass(slots=True)
class Admin(Account):
    ...


@dataclass(slots=True)
class Customer(Account):
    __bookings: list[Booking] = field(init=False, default_factory=list)
    
    @property
    def bookings(self):
        return self.__bookings

    def add_booking(self, booking: Booking):
        if booking.creator == self:
            self.bookings.append(booking)
    
    def get_booking(self, id: UUID):
        for booking in self.bookings:
            if booking.reference == id:
                return booking
        raise KeyError
    
    def view_booking(self, booking):
        info_list = []
        #Flight Infos
        temp_list = []
        for i in booking.reservation:
            temp_list.append([
                i.flight.date,
                i.flight.flight.departure,
                i.flight.flight.arrival,
                i.flight.flight.origin.name,
                i.flight.flight.origin.location_code,
                i.flight.flight.origin.city,
                i.flight.flight.origin.country,
                i.flight.flight.destination.name,
                i.flight.flight.destination.location_code,
                i.flight.flight.destination.city,
                i.flight.flight.destination.country,
                i.flight.aircraft.model,
                i.travel_class,

            ])
        info_list.append(temp_list)
        #Passenger Details
        temp_list = []
        for i in booking.passenger: #Get a list of list of passenger_detail attributes
            temp_list.append([
                i.forename,
                i.surname,
                i.birthday,
                i.gender,
                i.passport,
                i.passenger_type
            ])
        info_list.append(temp_list)
        #Contact Infos
        info_list.append([
            booking.contactinfo.name,
            booking.contactinfo.phone_country,
            booking.contactinfo.phone,
            booking.contactinfo.email,
        ])
        return info_list #return list