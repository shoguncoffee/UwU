"""
enum constants
"""
from enum import Enum

FlightStatus = Enum(
    'FlightStatus', 'SCHEDULED CANCELLED DELAYED IN_FLIGHT ARRIVED'
)
PassengerType = Enum(
    'PassengerType', 'ADULT CHILD INFANT'
)
TravelClass = Enum(
    'TravelClass', 'Economy Bussiness First'
)
AccountStatus = Enum(
    'AccountStatus', 'PENDING ACTIVE SUSPENDED'
)
BookingStatus = Enum(
    'BookingStatus', 'INCOMPLETE PENDING COMPLETE CANCELLED'
)
SeatType = Enum(
    'SeatType', 'STANDARD'
)
GenderType = Enum(
    'GenderType', 'MALE FEMALE'
)
PaymentStatus = Enum(
    'PaymentStatus', 'PENDING FAILED COMPLETED'
)
PaymentMethod = Enum(
    'PaymentMethod', 'PAYPAL INTERNETBANKING CREDITCARD'
)