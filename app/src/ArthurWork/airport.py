class Airport:

    def __init__(self, name, location_code, city, country):
        self.__name = name
        self.__location_code = location_code
        self.__city = city
        self.__country = country

    #getter
    def get_name(self):
        return self.__name

    def get_location_code(self):
        return self.__location_code
    
    def get_city(self):
        return self.__city
    
    def get_country(self):
        return self.__country