from base import *
if TYPE_CHECKING:
    from booking import Booking

@dataclass
class Person: 
    username: str
    name: str
    surname: str
    
    
class Employee(Person):
    position: ...
    

class Customer(Person):
    booking: list[Booking]
    privilege: ...
    payment: ...
    
    
class Pilot(Employee):
    ...
    

class Passenger(Customer):
    ...
    