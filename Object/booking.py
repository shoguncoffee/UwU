from base import *
if TYPE_CHECKING:
    from seat import Seat

@dataclass
class Booking:
    seats: list[Seat]
    status: ...