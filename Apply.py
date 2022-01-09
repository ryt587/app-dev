import User as u

class Apply(u.User):
    
    def __init__(self, email, password, address, address2, city, zip):
        super().__init__(email, password)
        self.__address=address
        self.__address2= address2
        self.__city= city
        self.__zip= zip
    
    def get_address(self):
        return self.__address
    
    def get_address2(self):
        return self.__address2
    
    def get_city(self):
        return self.__city
    
    def get_zip(self):
        return self.__zip
        
    def set_address(self, address):
        self.__address = address   
        
    def set_address2(self, address2):
        self.__address2 = address2
    
    def set_city(self, city):
        self.__city = city
    
    def set_zip(self, zip):
        self.__zip = zip
