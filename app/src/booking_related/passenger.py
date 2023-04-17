from __future__ import annotations
from ..base import *


@dataclass(slots=True)
class PassengerDetails:
    __forename: str # type: ignore
    __surname: str # type: ignore
    __birthdate: date # type: ignore
    __nationality: str # type: ignore
    __passport_id: str # type: ignore
    __gender: GenderType # type: ignore
    __passenger_type: PassengerType # type: ignore
    
    @property #Getter
    def forename(self):
        return self.__forename
    
    @forename.setter #Setter
    def forename(self, new_value):
        self.__forename = new_value
    
    @property #Getter
    def surname(self):
        return self.__surname
    
    @surname.setter #Setter
    def surname(self, new_value):
        self.__surname = new_value
    
    @property #Getter
    def birthday(self):
        return self.__birthdate.strftime('%d-%B-%Y')
    
    @birthday.setter #Setter
    def birthday(self, new_value):
        self.__birthdate = new_value
    
    @property #Getter
    def nationality(self):
        return self.__nationality
    
    @nationality.setter #Setter
    def nationality(self, new_value):
        self.__nationality = new_value

    @property #Getter
    def passport(self):
        return self.__passport_id
    
    @passport.setter #Setter
    def passport(self, new_value):
        self.__passport_id = new_value

    @property #Getter
    def gender(self):
        if self.__gender == GenderType.MALE:
            return 'Male'
        else:
            return 'Female'
    
    @gender.setter #Setter
    def gender(self, new_value):
        self.__gender = new_value

    @property #Getter
    def passenger_type(self):
        if self.__passenger_type == PassengerType.ADULT:
            return 'Adult'
        elif self.__passenger_type == PassengerType.CHILD:
            return 'Child'
        else:
            return 'Infant'
    
    @passenger_type.setter #Setter
    def passenger_type(self, new_value):
        self.__passenger_type = new_value

    @property
    def fullname(self):
        return f'{self.forename} {self.surname}'

    #def change_forename(self, name: str):
    #    self.__forename = name