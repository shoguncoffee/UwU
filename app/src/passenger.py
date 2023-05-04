from __future__ import annotations
from app.base import *


@dataclass(unsafe_hash=True)
class Passenger:
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


@dataclass
class ContactInformation:
    __passenger: Passenger # type: ignore
    __phone: str # type: ignore
    __email: str # type: ignore
    
    @property
    def passenger(self):
        return self.__passenger

    @property
    def phone(self):
        return self.__phone

    @property
    def email(self):
        return self.__email

    @property
    def name(self):
        return self.passenger.fullname


class Pax(tuple[tuple[PassengerType, int], ...]):
    """
    ### number of passengers for each type
        `tuple` of 
        (<PassengerType>, <int>) `->` "type of passenger", "number of passengers"
    """
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    
    def __len__(self):
        """
        total number of all passengers, including infants
        """
        return sum(
            number_of_passengers 
            for _, number_of_passengers in self
        )
    
    def get(self, passenger_type: PassengerType):
        """
        get number of passengers for a given type
        """
        for type, number_of_passengers in self:
            if type is passenger_type:
                return number_of_passengers
            
        raise KeyError
    
    @property
    def total(self):
        """
        total number of non-infant passengers
        """
        return sum(
            number for type, number in self 
            if type is not PassengerType.INFANT
        )
    
    @classmethod
    def count(cls, passengers: Iterable[Passenger]):
        """
        initialize Pax from a group of Passenger
        """
        types = [passenger.type for passenger in passengers]
        return cls(
            (type, types.count(type)) for type in set(types)
        )
        
    @classmethod
    def minimum(cls):
        """
        minimum Pax, by only one adult
        """
        return cls([(PassengerType.ADULT, 1)])