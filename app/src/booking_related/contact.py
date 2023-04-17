from __future__ import annotations
from ..base import *

if TYPE_CHECKING:
    from app.src import PassengerDetails


@dataclass(slots=True)
class ContactInformation:
    __passenger: PassengerDetails  # type: ignore
    __phone: str # type: ignore
    __phone_country: str # type: ignore
    __email: str # type: ignore
    
    @property #Getter
    def passenger(self):
        return self.__passenger
    
    @passenger.setter #Setter : NOTED
    def passenger(self, new_value):
        self.__passenger = new_value
 

    @property #Getter
    def phone(self):
        return self.__phone

    @phone.setter #Setter
    def phone(self, new_value):
        self.__phone = new_value


    @property #Getter
    def phone_country(self):
        return self.__phone_country
    
    @phone_country.setter #Setter
    def phone_country(self, new_value):
        self.__phone_country = new_value


    @property #Getter
    def email(self):
        return self.__email
    
    @email.setter #Setter
    def email(self, new_value):
        self.__email = new_value


    @property
    def name(self):
        return self.passenger.fullname
    
    def request_contact():
        pass

    def modify_contact():
        pass