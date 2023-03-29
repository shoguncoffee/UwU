from ..flightsystem.aflight import FlightInstance

class ScheduleDate :
    def __init__(self,date,schedule_flight) :
        self.__date = date
        self.__schedule_flight = []

    def create_flight_instance(self,date,flight,aircraft,base_price) :
        pass
    def get_flight_instance(self,origin,destination) :
        pass
    def remove_flight_instance(self,flight_instance) :
        pass
    def modify_flight_instance(self,aircraft,base_price,flight_instance) :
        pass
    def save_flight_instance(self) :
        self.__schedule_flight.append(self)