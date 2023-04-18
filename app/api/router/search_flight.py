"""
https://fastapi.tiangolo.com/tutorial/dependencies
"""
from .base import *

router = APIRouter(
    prefix="/search",
    tags=["searching"],
)


async def pax_parameters(
    adult: int = 1,
    child: int = 0,
    infant: int = 0,
):
    return src.Pax([
        (PassengerType.ADULT, adult),
        (PassengerType.CHILD, child),
        (PassengerType.INFANT, infant)
    ])
    
async def route_parameters(
    origin: Annotated[str, Query(max_length=3)],
    destination: Annotated[str, Query(max_length=3)]
):
    return [
        Airline.airports.get(code) 
        for code in (origin, destination)
    ]

Pax = Annotated[src.Pax, Depends(pax_parameters)]
Route = Annotated[tuple[src.Airport, src.Airport], Depends(route_parameters)]


@router.get("/one-way")
async def one_way_flight(
    route: Route,
    date: dt.date,
    pax: Pax,
):
    """
    - `origin`: `str "xxx"`
        - origin airport code
        
    - `destination`: `str "xxx"`
        - destination airport code
        
    - `date`: `str "yyyy-mm-dd"`
        - departure date
        
    - `adult`: `int`
    - `child`: `int`
    - `infant`: `int`
        - passenger number for each type
    """
    results = Airline.search_journey(
        *route, date, pax
    )
    return [
        FlightInfoBody.transforms(itinerary, pax) 
        for itinerary in results
    ]


@router.get("/return")
async def return_flight(
    route: Route,
    depart_date: dt.date,
    return_date: dt.date,
    pax: Pax,
):
    """
    - `origin`: `str "xxx"`
        - origin airport code
        
    - `destination`: `str "xxx"`
        - destination airport code
    
    - `depart_date`: `str "yyyy-mm-dd"`
        - first departure date
    
    - `return_date`: `str "yyyy-mm-dd"`
        - return date
        
    - `adult`: `int`
    - `child`: `int`
    - `infant`: `int`
        - passenger number for each type
    """
    return {
        'outbound': await one_way_flight(
            route, depart_date, pax
        ),
        'inbound': await one_way_flight(
            tuple(reversed(route)), return_date, pax
        )
    }