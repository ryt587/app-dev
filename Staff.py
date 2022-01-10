import User as u

class Staff(u.User):
    
    def __init__(self, staff_id, phone_number, email, password)
        super().__init__(email, password)
        self.__staff_id = staff_id
        self.__phone_number = phone_number
        
    def get_staff_id(self):
        return self.__staff_id
    
    def get_phone_number(self):
        return self.__phone_number
    
    
