"""

"""
from __future__ import annotations
from base import *
if TYPE_CHECKING:
    from booking import Booking

@dataslots
class Person: 
    forename: str
    surname: str

@dataslots
class CustomerProfile(Person):
    email: str
    booking: list[Booking]
    privilege: ...
    payment_method: ...

@dataslots
class Passenger(Person):
    date_of_birth: date
    nationality: str
    gender: ...

@dataslots
class Adult(Passenger):
    title: str
    travel_document: ...

@dataslots
class Infant(Passenger):
    ...

@dataslots
class Employee(Person):
    position: ...

@dataslots
class Pilot(Employee):
    ...