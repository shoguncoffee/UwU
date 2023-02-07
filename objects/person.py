"""
all impremented classes for person
"""
from __future__ import annotations
from base import *
if TYPE_CHECKING:
    import booking
    import privilege

Gender = Enum(
    'Human Gender',
    'MALE FEMALE'
)
class Age(Enum):
    """
    Age group
    
    e.g. ADULT = 12 => ADULT > 12 years
    """
    ADULT = 12
    CHILD = 2
    INFANT = 0
    
    def __new__(cls, age: int):
        for age_group in cls:
            if age > age_group.value:
                return age_group
    

@dataclass
class Person: 
    """
    a man
    """
    forename: str
    surname: str


@dataclass
class Customer(Person):
    """
    account profile for airline customer
    """
    email: str
    username: str
    passwrord: str
    booking: set[booking.Booking] # bag, cart
    payment_method: ...
    privilege: ...
    
    def as_passenger(self):
        return
    
    def login(self):
        ...

@dataclass
class Passenger(Person):
    """
    passenger of flight
    """
    date_of_birth: date
    nationality: str
    gender: Gender
    
    @property
    def age_group(self):
        delta = date.today() - self.date_of_birth
        age = round(delta.days / 365)
        return Age(age)


@dataclass
class Adult(Passenger):
    title: str
    travel_document: ...


@dataclass
class Infant(Passenger):
    """
    age <= 2
    """
    