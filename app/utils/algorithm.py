from __future__ import annotations
from datetime import timedelta
from app.base import *       

if TYPE_CHECKING:
    from app.src import *
    
    
def conjugate(
    *path: FlightInstance, 
    target: Airport,
    pool: Sequence[FlightInstance],
    limit: dt.timedelta,
) -> Generator[tuple[FlightInstance, ...], None, None]:
    """
    find all possible sequence of FlightInstance 
    that can take from origin to destination in limit duration
    """
    cumulative_time = sum(
        [inst.flight.duration for inst in path], 
        start=dt.timedelta()
    )
    prev_instance = path[-1]
    prev_flight = prev_instance.flight
    
    for instance in pool:
        this_flight = instance.flight
        arrival_time = dt.datetime.combine(prev_instance.date, prev_flight.arrival)
        depart_time = dt.datetime.combine(instance.date, this_flight.departure)
        transit_time = depart_time - arrival_time
        
        if this_flight.origin is prev_flight.destination and transit_time > timedelta() and instance not in path:
            if cumulative_time + transit_time + this_flight.duration < limit:
                if this_flight.destination is target:
                    yield *path, instance
                    
                else:
                    yield from conjugate(
                        *path, instance, 
                        target=target, 
                        pool=pool, 
                        limit=limit
                    )