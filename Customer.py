import User as u
from datetime import date

class Customer(u.User):
    count_id=0
    
    def __init__(self, first_name, last_name, password, email, address):
        super().__init__(email, password)
        self.__class__.count_id+=1
        self.__customer_id=self.__class__.count_id
        self.__first_name=first_name
        self.__last_name=last_name
        self.__date_joined=date.today().strftime("%d/%m/%Y")
        self.__address= address
        
    def get_customer_id(self):
        return self.__customer_id

    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name
    
    def get_date_joined(self):
        return self.__date_joined
    
    def get_address(self):
        return self.__address
    
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id
        
    def set_first_name(self, first_name):
        self.__email = first_name
        
    def set_last_name(self, last_name):
        self.__email = last_name
    
    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined
        
    def set_address(self, address):
        self.__address = address
