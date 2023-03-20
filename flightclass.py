class FlightSchduling:
    def __init__(self, advance_days):
        self.__plans = []
        self.__advance_days = advance_days

    def create_flight_plan(self, flightplan):
        pass
    
class FlightCatalog:
    def __init__(self):
        self.__records = []
        
    def create_flight(self, flight):
        pass
    
    def update_records(self):
        pass
    
    def remove_flight(self, flight):
        pass
    
    def search_flight(self, date, origin, destination):
        pass
    
class Flight:
    def __init__(self, designator, departure, arrival, origin, destination, reference):
        self.__designator = designator
        self.__departure = departure
        self.__arrival = arrival
        self.__origin = origin
        self.__destination = destination
        self.__reference = reference   

class FlightPlan:
    def __init__(self, flight, start_date, end_date, exception):
        self.__flight = flight
        self.__start_date = start_date
        self.__end_date = end_date
        self.__exception = exception
        
class Deviation:
    def __init__(self, weekday, months, dates):
        self.__weekdays = weekday
        self.__months = months
        self.__dates = dates
