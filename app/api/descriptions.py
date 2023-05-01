from app.constants import *

travel_class: dict[TravelClass, list[str]] = {
    TravelClass.ECONOMY: [
        'economy',
    ],
    TravelClass.BUSSINESS: [
        'bussiness',
    ],
    TravelClass.FIRST: [
        'first',
    ],
}

seat: dict[SeatType, list[str]] = {
    SeatType.WINDOW: [
        'window',
    ],
    SeatType.AISLE: [
        'aisle',
    ],
    SeatType.LEGROOM: [
        'middle',
    ],
} #!