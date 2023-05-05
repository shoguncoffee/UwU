from __future__ import annotations
from app.base import *

if TYPE_CHECKING:
    from . import Booking


@dataclass
class Account:
    __username: str # type: ignore
    __password: str # type: ignore
    __email: str # type: ignore
    __phone: str # type: ignore
    __status: AccountStatus = field(init=False, default=AccountStatus.INACTIVE)
    
    @property
    def username(self):
        return self.__username
    
    @property
    def email(self):
        return self.__email
    
    @property
    def phone(self):
        return self.__phone
    
    @property
    def status(self):
        return self.__status

    @property
    def password(self):
        return self.__password


@dataclass
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