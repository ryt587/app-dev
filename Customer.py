import User as u
import shelve

class Customer(u.User):
    
    def __init__(self, first_name, last_name, password, email, birthdate, address, postal, city):
        db = shelve.open('user.db', 'c')
        users_dict={}
        try:
            if 'Users' in db:
                users_dict=db['Users']
            else:
                db['Users']=users_dict
            if users_dict=={}:
                id=1
            else:
                id='C1'
                while id in users_dict:
                    id=id[:1]+str(int(id[2:])+1)
        except:
            print("Error in retrieving Users from user.db.")
        db.close()
        super().__init__(first_name, email, password)
        self.__user_id=id
        self.__last_name=last_name
        self.__birthdate=birthdate
        self.__address= address
        self.__postal= postal
        self.__city= city
    
    def get_user_id(self):
        return self.__user_id
    
    def get_last_name(self):
        return self.__last_name
    
    def get_birthdate(self):
        return self.__birthdate
    
    def get_address(self):
        return self.__address
    
    def get_postal(self):
        return self.__postal
    
    def get_city(self):
        return self.__city
    
    def set_user_id(self, user_id):
        self.__user_id = user_id
        
    def set_last_name(self, last_name):
        self.__last_name = last_name
        
    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate
        
    def set_address(self, address):
        self.__address = address
        
    def set_postal(self, postal):
        self.__postal = postal
        
    def set_city(self, city):
        self.__city = city
