from app.utils.packages import *
from app.constants import *

if TYPE_CHECKING:
    T = TypeVar('T')
    U = TypeVar('U')
    
    
def daterange(days: int, start: Optional[dt.date] = None):
    """
    if start is None, start = dt.date.today()
    
    *include start and end
    """
    start = start or dt.date.today()
    for i in range(days + 1):
        yield start + dt.timedelta(i)