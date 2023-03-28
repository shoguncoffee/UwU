class Airport:

    def __init__(self, name, location_code, city, country):
        self.__name = name
        self.__location_code = location_code
        self.__city = city
        self.__country = country

    @property
    def name(self):
        return self.__name
    
    @property
    def location_code(self):
        return self.__location_code
    
    @property
    def city(self):
        return self.__city
    
    @property
    def country(self):
        return self.__country
