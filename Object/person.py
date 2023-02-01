from base import *
if TYPE_CHECKING:
    from booking import Booking

@dataclass
class Person: 
    forename: str
    surname: str
    

class CustomerProfile(Person):
    email: str
    booking: list[Booking]
    privilege: ...
    payment_method: ...

class Passenger(Person):
    date_of_birth: date
    nationality: str
    gender: ...
    
    
class Adult(Passenger):
    title: str
    travel_document: ...
    
    
class Infant(Passenger):
    ...
    
class Employee(Person):
    position: ...
    
class Pilot(Employee):
    ...