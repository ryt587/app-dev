import User as u
import shelve

class Staff(u.User):
    
    def __init__(self, name, email, password, staff_role, phone_number):
        db = shelve.open('user.db', 'c')
        users_dict={}
        try:
            if 'Staffs' in db:
                users_dict=db['Staffs']
            else:
                db['Staffs']=users_dict
            if users_dict=={}:
                id=1
            else:
                id=1
                while id in users_dict:
                    id+=1
        except:
            print("Error in retrieving Users from user.db.")
        db.close()
        super().__init__(name, email, password)
        self.__staff_id = 'St'+str(id)
        self.__staff_role = staff_role
        self.__phone_number = phone_number
    
    def get_staff_id(self):
        return self.__staff_id
    
    def get_phone_number(self):
        return self.__phone_number
    
    def get_staff_role(self):
        return self.__staff_role
    
    def set_staff_id(self,staff_id):
        self.__staff_id = staff_id
    
    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number
        
    def set_staff_role(self, staff_role):
        self.__staff_role = staff_role
    
    
