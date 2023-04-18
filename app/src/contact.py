from __future__ import annotations
from .base import *

if TYPE_CHECKING:
    from app.src import PassengerDetails


@dataclass(slots=True)
class ContactInformation:
    __passenger: PassengerDetails # type: ignore
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