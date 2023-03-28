from __future__ import annotations
from app.base import *

from ..constants import GenderType, PassengerType

@dataclass
class PassengerDetail:
    __forename: str #type:ignore
    __surname: str #type:ignore
    __birthdate: date #type:ignore
    __gender: GenderType #type:ignore
    __passport_id: str #type:ignore
    __passenger_type: PassengerType #type:ignore
    __nationality: str #type:ignore
 
    def request_passenger_detail(self):
        pass

    def modify_passenger_detail(self):
        pass

    def create_passenger_detail(self):
        pass

    #Getter zone
    def get_passenger_fullname(self): #getter
        return self.__forename + ' ' + self.__surname
    
    #def get_forename(self):
    #    return self.__forename
    
    #def get_surname(self):
    #    return self.__surname
    
    def get_birthday(self):
        return self.__birthdate
    
    def get_gender(self):
        return self.__gender
    
    def get_passport(self):
        return self.__passport_id
    
    def get_passenger_type(self):
        return self.__passenger_type
    
    def get_nationality(self):
        return self.__nationality