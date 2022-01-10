import User as u

class Staff(u.User):
    
    def __init__(self, staff_id, email, password)
        super().__innit__(email, password)
        self.__staff_id = staff_id
        
    def get_staff_id(self):
        return self.__staff_id
