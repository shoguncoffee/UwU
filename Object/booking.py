from base import *
if TYPE_CHECKING:
    from seat import Seat

STATUS = Enum(
    'status', 
    'PAID CHECK'
)

@dataclass
class Booking:
    seats: list[Seat]
    status: STATUS
    
    
if __name__ != '__main__':
    globals().update(STATUS.__members__)