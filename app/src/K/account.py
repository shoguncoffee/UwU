from __future__ import annotations
from ..base import *

if TYPE_CHECKING:
    from app.src import Booking, Trip, ContactInformation, PassengerDetails

@dataclass(slots=True)
class Account:
    _username: str
    _password: str
    _email: str
    _phone: str
    _status: AccountStatus = field(init=False, compare=False, default=AccountStatus.PENDING)
    # __reference: str = field(init=False)
    
    @property
    def username(self):
        return self._username
    
    @property
    def email(self):
        return self._email
    
    @property
    def password(self):
        return self._password
    
    @property
    def status(self):
        return self._status
    
    
@dataclass(slots=True)
class Customer(Account):
    __bookings: list[Booking] = field(init=False, default_factory=list)
    
    @property
    def bookings(self):
        return self.__bookings


    def request_booking(self,
        journey: list[Trip],
        contact: ContactInformation,
        *passenger: PassengerDetails,
    ):
        if self.status != AccountStatus.PENDING:
            from app.system import Airline
            Airline.create_booking(
                self, 
                journey, 
                contact, 
                *passenger, 
            )

    def add_booking(self, booking: Booking):
        print("Status Report : Add Booking Completed") #Delete later
        self.__bookings.append(booking)            
    

    def select_booking(self, num):
        if (int(num) > len(self.__bookings) or int(num) <= 0):
            print("This booking doesn't exist.")
        else:
            print("Status Report : Select Booking Completed") #Delete later
            return self.__bookings[int(num) - 1]
            
            
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

    def modify_booking(self):
        pass
    
    
@dataclass(slots=True)
class Admin(Account):
    def request(self):
        ...