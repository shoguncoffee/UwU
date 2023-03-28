from flightsystem.aflight import FlightInstance
class ScheduleDate :
    def __init__(self,date,schedule_flight) :
        self.__date = date
        self.__schedule_flight = []

    def create_flight_instance(self) :
        pass
    def get_flight_instance(self) :
        pass
    def remove_flight_instance(self,flight_instance) :
        pass
    def modify_flight_instance(self) :
        pass
    def save_flight_instance(self) :
        self.__schedule_flight.append(self)