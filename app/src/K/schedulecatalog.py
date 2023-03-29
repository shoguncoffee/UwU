class ScheduleCatalog :
    def __init__(self,records) :
        self.__records = []
    
    def add_new_date(self,schedule_date) :
        self.__records.append(schedule_date)
    def delete_history(self) :
        pass
    def search_flight(self,date,origin,destination,passenger_no) :
        pass
    def get_possible_schedule_date(self,date) :
        for i in self.__records :
            pass
    def match_flight_itinerary_between_airport(self) :
        pass
    def create_flight_instance(self,date,flight,aircraft,base_price) :
        pass
    def get_flight_instance(self,origin,destination) :
        pass
    def modify_flight_instance(self,aircraft,base_price,flight_instance) :
        pass