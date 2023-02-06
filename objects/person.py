"""

"""
from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from booking import Booking
    from privilege import Privilege

@dataclass
class Person: 
    """
    a man
    """
    forename: str
    surname: str


@dataclass
class Account:
    """
    
    """
    username: str
    password: str
    
    def login(self):
        ...


@dataclass
class Customer(Person):
    """
    account profile for customer
    """
    email: str
    booking: list[Booking] # bag, cart
    payment_method: ...
    privilege: ...
    
    def as_passenger(self):
        return

@dataclass
class Passenger(Person):
    date_of_birth: date
    nationality: str
    gender: ...

@dataclass
class Adult(Passenger):
    title: str
    travel_document: ...

@dataclass
class Infant(Passenger):
    ...