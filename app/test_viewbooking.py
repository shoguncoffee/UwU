#Created by Sai on 26/03/2023

#Testing view booking
#Assuming we have a booking already
#Generization about this view booking is that a customer holds a booking at the current time and he needs to choose which booking
#he wants to view and now that he chose a booking then he proceed to get all the important information to view
# Each passenger details (forename, surname, date of birth, gender, passport id, passenger type, nationality)
# Contact information (owner's name, phone number, country of phone number, email)
# Each flight details (origin, destination, designation, departure, arrival) > flight airport aircraft
# For each aircraft there needs be model

import datetime

from .src import AccountStatus
from .src import GenderType
from .src import PassengerType
from .src import TravelClass

from .src import Booking
from .src import ContactInformation
from .src import Customer
from .src import PassengerDetail
from .src import FlightReservation
from .src import Aircraft
from .src import Airport
from .src import Flight
from .src import FlightInstance
from .src import SeatReservation

#create a test customer account
customer_1 = Customer("Testing", "test@test.com", "001", "password", AccountStatus.ACTIVE, "0123456789")

#Create passenger detail manually
passenger_detail_1 = PassengerDetail("Somchai", "Fahchaiyaphum", datetime.date(1999, 5, 17), GenderType.MALE, "T00000001", PassengerType.ADULT, "Thai") #Nationality must come from database
passenger_detail_2 = PassengerDetail("Somsri", "Rattanasiri", datetime.date(1997, 11, 30), GenderType.FEMALE, "T00000002", PassengerType.ADULT, "Thai") #Nationality must come from database


#Create contact info manually
contact_info_1 = ContactInformation(passenger_detail_1.get_passenger_fullname(), "0123456789", "Thailand", "test@test.com")

#Create aircraft
aircraft_1 = Aircraft("Boeing717", "FAA", None)

#Create airport
airport_1 = Airport("Suvarnabhumi Airport", "BKK", "Bangkok", "Thailand")
airport_2 = Airport("Homad International Airport", "DOH", "Doha", "Qatar")
airport_3 = Airport("London City Airport", "LCA", "London", "United Kingdom")

#Create flight
flight_1 = Flight("Q001", datetime.time(8, 0), datetime.time(15, 20), airport_1, airport_2)
flight_2 = Flight("Q002", datetime.time(17, 10), datetime.time(22, 30), airport_2, airport_3)
flight_3 = Flight("Q003", datetime.time(13, 15), datetime.time(18, 35), airport_3, airport_2)
flight_4 = Flight("Q004", datetime.time(21, 5), datetime.time(4, 25), airport_2, airport_1)

#Create flight instances
flightin_1 = FlightInstance(flight_1, datetime.date(2023, 1, 18), aircraft_1, 50000)
flightin_2 = FlightInstance(flight_2, datetime.date(2023, 1, 18), aircraft_1, 40000)
flightin_3 = FlightInstance(flight_3, datetime.date(2023, 1, 23), aircraft_1, 50000)
flightin_4 = FlightInstance(flight_4, datetime.date(2023, 1, 23), aircraft_1, 40000)

#Create flight reservation
flightrev_1 = FlightReservation(TravelClass.ECONOMY, flightin_1)
flightrev_2 = FlightReservation(TravelClass.ECONOMY, flightin_2)
flightrev_3 = FlightReservation(TravelClass.ECONOMY, flightin_3)
flightrev_4 = FlightReservation(TravelClass.ECONOMY, flightin_4)

#Create Reserved Seat
flightrev_1.create_reserved_seat(passenger_detail_1, None)
flightrev_1.create_reserved_seat(passenger_detail_2, None)
flightrev_2.create_reserved_seat(passenger_detail_1, None)
flightrev_2.create_reserved_seat(passenger_detail_2, None)
flightrev_3.create_reserved_seat(passenger_detail_1, None)
flightrev_3.create_reserved_seat(passenger_detail_2, None)
flightrev_4.create_reserved_seat(passenger_detail_1, None)
flightrev_4.create_reserved_seat(passenger_detail_2, None)

#Create a booking
booking_1 = Booking(customer_1, "001", datetime.date(2023, 1, 12), contact_info_1, 45000.00)
booking_1.add_passenger_detail(passenger_detail_1)
booking_1.add_passenger_detail(passenger_detail_2)

booking_1.add_flight_reservation(flightrev_1)
booking_1.add_flight_reservation(flightrev_2)
booking_1.add_flight_reservation(flightrev_3)
booking_1.add_flight_reservation(flightrev_4)


customer_1.add_booking(booking_1)


#Start here
booking_num = input("Please input your booking number start with 1 : ")

book = customer_1.select_booking(booking_num)

if book != None:
    book.view_booking()