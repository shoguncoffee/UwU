from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from ..constants import GenderType, PassengerType

@dataclass
class PassengerDetails:
    __forename: str # type: ignore
    __surname: str # type: ignore
    __birthdate: date # type: ignore
    __gender: GenderType # type: ignore
    __passport_id: str # type: ignore
    __passenger_type: PassengerType # type: ignore
    __nationality: str # type: ignore
    
    @property
    def forename(self):
        return self.__forename
    
    @property
    def surname(self):
        return self.__surname
    
    @property
    def birthday(self):
        return self.__birthdate
    
    @property
    def gender(self):
        return self.__gender
    
    @property
    def passport(self):
        return self.__passport_id
    
    @property
    def passenger_type(self):
        return self.__passenger_type
    
    @property
    def nationality(self):
        return self.__nationality
    
    
    @property
    def fullname(self):
        return f'{self.forename} {self.surname}'
    
    def request_passenger_detail():
        pass

    def modify_passenger_detail():
        pass