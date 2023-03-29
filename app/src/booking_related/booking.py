from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from .customer import Customer
    from .passenger_detail import PassengerDetails
    from .flight_reservation import FlightReservation
    from .contact_information import ContactInformation
from ..constants import BookingStatus
        
class Bookingold:
    def __init__(self, creator: Customer, reference, contact_info: ContactInformation):
        self.__creator = creator
        self.__reference = reference
        self.__contact_info = contact_info
        self.__reserved_flights = []
        self.__passenger_details = []
        self.__ticket_ref = []
        self.__status: BookingStatus = BookingStatus.PENDING
        self.__total_fare = self.get_price()

    def get_price(self):
        ...
    
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


@dataclass
class Booking: #(HasReference):
    __creator: Customer # type: ignore
    __reservation: list[FlightReservation] # type: ignore
    __passenger: list[PassengerDetails] # type: ignore
    __contactinfo: ContactInformation # type: ignore
    # __reference: Optional[UUID] = reference or self.generate_reference() # type: ignore
    __status: Optional[BookingStatus] = None # type: ignore
    
    __date: date = field(init=False, default_factory=date.today)
    
    
    def __post_init__(self):
        self.__status = self.status or self.init_status()
        
    def init_status(self):
        if all(reserve.is_selected for reserve in self.reservation):
            return BookingStatus.PENDING
        
        return BookingStatus.INCOMPLETE

    @property
    def creator(self):
        return self.__creator
                
    @property
    def reservation(self):
        return self.__reservation
    
    @property
    def passenger(self):
        return self.__passenger
    
    @property
    def contactinfo(self):
        return self.__contactinfo
        
    @property
    def status(self):
        return self.__status
    
    @property
    def creation_date(self):
        return self.__date
    
    @property
    def passenger_number(self):
        return len(self.passenger)