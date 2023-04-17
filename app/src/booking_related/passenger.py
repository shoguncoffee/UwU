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
    
    @property
    def forename(self):
        return self.__forename
    
    @property
    def surname(self):
        return self.__surname
    
    @property
    def birthdate(self):
        return self.__birthdate
    
    @property
    def gender(self):
        return self.__gender
    
    @property
    def passport_id(self):
        return self.__passport_id
    
    @property
    def type(self):
        return self.__type
    
    @property
    def nationality(self):
        return self.__nationality
    
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