from __future__ import annotations
from app.base import *

@dataclass
class ContactInformation:
    __name: str #type:ignore
    __phone: str #type:ignore
    __phone_country: str #type:ignore
    __email: str #type:ignore

    def request_contact_information(self):
        pass

    def modify_contact_information(self):
        pass

    def create_contact_information(self):
        pass


    def get_name(self):
        return self.__name
    
    def get_phone(self):
        return self.__phone
    
    def get_phone_country(self):
        return self.__phone_country
    
    def get_email(self):
        return self.__email