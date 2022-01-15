import User as u
import shelve

class Apply(u.User):
    
    def __init__(self, name, email, password, address, address2, city, postal, image):
        db = shelve.open('user.db', 'c')
        users_dict={}
        try:
            if 'Users' in db:
                users_dict=db['Applications']
            else:
                db['Applications']=users_dict
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
        self.__apply_id=id
        self.__address=address
        self.__address2= address2
        self.__city= city
        self.__postal= postal
        self.__image= image
    
    def get_apply_id(self):
        return self.__apply_id
    
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
        
    def set_apply_id(self, apply_id):
        self.__apply_id = apply_id 
    
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
