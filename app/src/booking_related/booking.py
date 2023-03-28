from __future__ import annotations
from app.base import *

from ..constants import BookingStatus
from .customer import Customer
from .contact_information import ContactInformation
from .passenger_detail import PassengerDetail
from .flight_reservation import FlightReservation
import math

@dataclass
class Booking:
    __creator: Customer #type:ignore
    __reference: str #type:ignore
    __date: date #type:ignore
    __contact_info: ContactInformation #type:ignore
    __total_fare: float #type:ignore #total fare should be added via create booking sequence 
    __reserved_flights: list[FlightReservation] = field(default_factory=list) #type:ignore
    __passenger_details: list[PassengerDetail] = field(default_factory=list) #type:ignore
    __ticket_ref: list[str] = field(default_factory=list) #type:ignore
    __status: BookingStatus = BookingStatus.PENDING #type:ignore


    def get_all_flight(self):
        pass

    def is_connecting_flight(self):
        pass

    def calculate_fare(self):
        pass

    def create_payment(self):
        pass

    def request_modify_booking(self):
        pass

    #def modify_booking():
    #    pass

    #def create_booking():
    #    pass

    def fill_information(self):
        pass

    #def cancel_booking():
    #    pass

    def add_flight_reservation(self, flight_reservation): #Temporary Awaiting create_booking sequence
        self.__reserved_flights.append(flight_reservation)


    def add_passenger_detail(self, passenger_detail): #Temporary Awaiting create_booking sequence
        self.__passenger_details.append(passenger_detail)


    def view_booking(self):
        #get booking info
        print('-------------------------------------')
        #print('Booking created by {}'.format(self.__creator.get_username()))
        print('Reference Number : {}'.format(self.__reference))
        print('Created on {}'.format(self.__date))
        print('Total fare : {}'.format(self.__total_fare))

        #get flight information
        print('-------------------------------------')
        print('Flight Information')
        for i in self.__reserved_flights:
            print('-------------------------------------')
            print('Flight {}'.format(self.__reserved_flights.index(i) + 1))
            print('Departure : {}, {} --- {}, {}, {}'.format(
                    i.get_flight_instance().get_date(),
                    i.get_flight_instance().get_flight().get_departure(), 
                    i.get_flight_instance().get_flight().get_origin().get_city(),
                    i.get_flight_instance().get_flight().get_origin().get_name(),
                    i.get_flight_instance().get_flight().get_origin().get_country())
                )
            print('Arrival : {}, {} --- {}, {}, {}'.format(
                    i.get_flight_instance().get_date(),
                    i.get_flight_instance().get_flight().get_arrival(), 
                    i.get_flight_instance().get_flight().get_destination().get_city(),
                    i.get_flight_instance().get_flight().get_destination().get_name(),
                    i.get_flight_instance().get_flight().get_destination().get_country())
                )
            duration = i.get_flight_instance().get_flight().duration
            total_second = duration.seconds
            remaining_minute = math.floor(total_second / 60) - (math.floor(math.floor(total_second / 60) / 60) * 60)
            total_hour = math.floor(math.floor(total_second / 60) / 60)
            print('Total flight time {} hours'.format(total_hour), end =" ")
            if int(remaining_minute) != 0:
                print('and {} minutes'.format(remaining_minute))

            print('Travel class : {}'.format(i.get_travel_class()))
            
        #get passenger details
        print('-------------------------------------')
        print('Passenger Information')
        for i in self.__passenger_details:
            print('-------------------------------------')
            print("Passenger {} : ".format(self.__passenger_details.index(i) + 1))
            print("Name : {}".format(i.get_passenger_fullname()))
            print("Birth : {}".format(i.get_birthday()))
            print("Gender : {}".format(i.get_gender()))
            print("Passport : {}".format(i.get_passport()))
            print("Passenger type : {}".format(i.get_passenger_type()))
            print("Nationality : {}".format(i.get_nationality()))

        #get contact information
        print('-------------------------------------')
        print('Contact Information')
        print('-------------------------------------')
        print("Name : {}".format(self.__contact_info.get_name()))
        print("Phone : {}".format(self.__contact_info.get_phone()))
        print("Phone nationality : {}".format(self.__contact_info.get_phone_country()))
        print("Email : {}".format(self.__contact_info.get_email()))

        #get reserved seat information
        print('-------------------------------------')
        print('Seats')
        print('-------------------------------------')
        for i in self.__reserved_flights:
            print('{} to {}'.format(i.get_flight_instance().get_flight().get_origin().get_location_code(), 
                                    i.get_flight_instance().get_flight().get_destination().get_location_code()))
            for j in i.get_all_reserved_seat():
                print('Name : {} - Seat : {}'.format(j.get_owner_name(), j.get_seat_pos()))