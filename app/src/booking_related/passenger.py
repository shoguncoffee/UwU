from __future__ import annotations
from ..base import *


@dataclass(slots=True, unsafe_hash=True)
class PassengerDetails:
    __forename: str # type: ignore
    __surname: str # type: ignore
    __birthdate: dt.date # type: ignore
    __nationality: str # type: ignore
    __passport_id: str # type: ignore
    __gender: GenderType # type: ignore
    __type: PassengerType # type: ignore
    
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
    def birthdate(self):
        return self.__birthdate
    
    @birthdate.setter #Setter
    def birthdate(self, new_value):
        self.__birthdate = new_value
    
    @property #Getter
    def nationality(self):
        return self.__nationality
    
    @nationality.setter #Setter
    def nationality(self, new_value):
        self.__nationality = new_value

    @property #Getter
    def passport_id(self):
        return self.__passport_id
    
    @passport_id.setter #Setter
    def passport_id(self, new_value):
        self.__passport_id = new_value

    @property #Getter
    def gender(self):
        return self.__gender

    
    @gender.setter #Setter
    def gender(self, new_value):
        self.__gender = new_value

    @property #Getter
    def type(self):
        return self.__type

    
    @type.setter #Setter
    def type(self, new_value):
        self.__type = new_value

    @property
    def fullname(self):
        return f'{self.forename} {self.surname}'

    def change_forename(self, name: str):
        self.__forename = name
    
    
class Pax(tuple[tuple[PassengerType, int], ...]):
    """
    (PassengerType, number)
    """
    def get(self, passenger_type: PassengerType):
        for type, number in self:
            if type == passenger_type:
                return number
        raise KeyError
    
    @property
    def total_capable(self):
        """
        non-infant passengers
        """
        return sum(
            number for type, number in self 
            if type is not PassengerType.INFANT
        )
    
    @classmethod 
    def init(cls, passengers: Sequence[PassengerDetails]):
        types = [passenger.type for passenger in passengers]
        return cls(
            (type, types.count(type)) 
            for type in PassengerType if type in types
        )