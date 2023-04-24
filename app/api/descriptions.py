from app.constants import *

travel_class: dict[TravelClass, tuple[str, ...]] = {
    TravelClass.ECONOMY: (
        'economy',
    ),
    TravelClass.BUSSINESS: (
        'bussiness',
    ),
    TravelClass.FIRST: (
        'first',
    ),
}

seat: dict[SeatType, tuple[str, ...]] = {
    SeatType.WINDOW: (
        'window',
    ),
    SeatType.AISLE: (
        'aisle',
    ),
    SeatType.LEGROOM: (
        'middle',
    ),
} #!