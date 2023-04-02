from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from app.src import *

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
    __bookings: set[Booking] = field(init=False, default_factory=set)
    
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
        self.__bookings.add(booking)            
    
    def selected_booking(self, num):
        ...
            
    def view_booking(self):
        ...
    
    
@dataclass(slots=True)
class Admin(Account):
    def request(self):
        ...