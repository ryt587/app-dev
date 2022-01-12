import User as u

class Apply(u.User):
    
    def __init__(self, email, password, address, address2, city, postal, image):
        super().__init__(email, password)
        self.__address=address
        self.__address2= address2
        self.__city= city
        self.__postal= postal
        self.__image= image
    
    def get_address(self):
        return self.__address
    
    def get_address2(self):
        return self.__address2
    
    def get_city(self):
        return self.__city
    
    def get_postal(self):
        return self.__postal
        
    def get_image(self):
        return self.__image    
        
    def set_address(self, address):
        self.__address = address   
        
    def set_address2(self, address2):
        self.__address2 = address2
    
    def set_city(self, city):
        self.__city = city
    
    def set_postal(self, postal):
        self.__postal = postal
    
    def set_image(self, image):
        self.__image = image
