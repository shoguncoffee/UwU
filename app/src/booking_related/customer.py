from src import Account
from booking import Booking

class Customer(Account):

    def __init__(self, username, email, reference, password, status, phone):
        Account.__init__(self, username, email, reference, password, status)
        self.__phone = phone
        self.__bookings = []

        
    def select_booking(self, num):
        while (num > len(self.__bookings)):
            print("This booking doesn't exist currently.")
        else:
            return self.__bookings[num - 1]
            

    def view_booking():
        pass


    def add_booking(self, booking): #Temporary
        self.__bookings.append(booking)