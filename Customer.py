import User as u
from datetime import date


class Customer(u.User):
    
    def __init__(self, first_name, last_name, password, email, birthdate, address, postal, city):
        super().__init__(email, password)
        self.__first_name=first_name
        self.__last_name=last_name
        self.__birthdate=birthdate
        self.__date_joined=date.today().strftime("%d/%m/%Y")
        self.__address= address
        self.__postal= postal
        self.__city= city
    
    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name
    
    def get_birthdate(self):
        return self.__birthdate
    
    def get_date_joined(self):
        return self.__date_joined
    
    def get_address(self):
        return self.__address
    
    def get_postal(self):
        return self.__postal
    
    def get_city(self):
        return self.__city
        
    def set_first_name(self, first_name):
        self.__first_name = first_name
        
    def set_last_name(self, last_name):
        self.__last_name = last_name
        
    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate
    
    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined
        
    def set_address(self, address):
        self.__address = address
        
    def set_postal(self, postal):
        self.__postal = postal
        
    def set_city(self, city):
        self.__city = city
