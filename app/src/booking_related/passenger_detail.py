class PassengerDetail:
    def __init__(self, forename, surname, birthdate, gender, passport_id, passenger_type, nationality, travel_document=None):
        self.__forename = forename
        self.__surname = surname
        self.__birthdate = birthdate
        self.__gender = gender
        self.__passport_id = passport_id
        self.__passenger_type = passenger_type
        self.__nationality = nationality
        self.__travel_document = travel_document

    def request_passenger_detail():
        pass

    def modify_passenger_detail():
        pass

    def create_passenger_detail():
        pass

    #Getter zone
    def get_passenger_fullname(self): #getter
        return self.__forename + ' ' + self.__surname
    
    def get_forename(self):
        return self.__forename
    
    def get_surname(self):
        return self.__surname
    
    def get_birthday(self):
        return self.__birthdate
    
    def get_gender(self):
        return self.__gender
    
    def get_passport(self):
        return self.__passport_id
    
    def get_passenger_type(self):
        return self.__passenger_type
    
    def get_nationality(self):
        return self.__nationality
    
    def get_travel_document(self):
        return self.__travel_document