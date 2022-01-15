import shelve
from datetime import date


class User: 
        
    def __init__(self, name, email, password):
        self.__name=name
        self.__email=email
        self.__password=password
        self.__date_joined=date.today().strftime("%Y-%m-%d")
      
    def get_name(self):
        return self.__name
    
    def get_email(self):
        return self.__email
      
    def get_password(self):
        return self.__password
    
    def get_date_joined(self):
        return self.__date_joined
    
    def set_name(self, name):
        self.__name = name
    
    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password
    
    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined
