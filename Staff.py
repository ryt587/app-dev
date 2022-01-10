import User as u

class Staff(u.User):
    
    def __init__(self, staff_role phone_number, email, password)
        super().__init__(email, password)
        self.__staff_role = staff_role
        self.__phone_number = phone_number
    
    def get_phone_number(self):
        return self.__phone_number
    
    def get_staff_role(self):
        return self.__staff_role
    
    
    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number
        
    def set_staff_role(self, staff_role):
        self.__staff_role = staff_role
    
    
