from __future__ import annotations
from .base import *

if TYPE_CHECKING:
    from app.src import *
    

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
    
    def get_booking(self, id: UUID):
        for booking in self.bookings:
            if booking.reference == id:
                return booking
            
        raise KeyError