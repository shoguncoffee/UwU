from ..constants import BookingStatus
from .contact_information import ContactInformation
from .passenger_detail import PassengerDetail

class Booking:
    def __init__(self, creator, reference, contact_info, total_fare, status=BookingStatus.PENDING):
        self.__creator = creator
        self.__reference = reference
        self.__status = status
        self.__contact_info = contact_info
        self.__total_fare = total_fare #total fare should be added via create booking sequence
        self.__reserved_flights = []
        self.__passenger_details = []
        self.__ticket_ref = []

    def get_all_flight():
        pass

    def is_connecting_flight():
        pass

    def calculate_fare():
        pass

    def create_payment():
        pass

    def request_modify_booking():
        pass

    #def modify_booking():
    #    pass

    #def create_booking():
    #    pass

    def fill_information():
        pass

    #def cancel_booking():
    #    pass

    def add_passenger_detail(self, passenger_detail): #Temporary
        self.__passenger_details.append(passenger_detail)

    #main dish boii
    '''
    def view_booking(self):
        #get passenger details
        count = 1
        for i in self.__passenger_details:
            print("Passenger {} : ".format(count))
            print(i.get_forename())
            print(i.get_surname())
            print(i.get_birthday())
            print(i.get_gender())
            print(i.get_passport())
            print(i.get_passenger_type())
            print(i.get_nationality())
            if i.get_travel_document() != None:
                print(i.get_travel_document())

    '''
        #get contact information
        