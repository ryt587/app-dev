import User as u
import shelve

class Seller(u.User):
  
    def __init__(self, name, email, password, address, address2, city, postal_code):
        db = shelve.open('user.db', 'c')
        users_dict={}
        try:
            if 'Users' in db:
                users_dict=db['Users']
            else:
                db['Users']=users_dict
            if users_dict=={}:
                id='Se1'
            else:
                id='Se1'
                while id in users_dict:
                    id=id[:2]+str(int(id[2:])+1)
        except:
            print("Error in retrieving Users from user.db.")
        db.close()
        super().__init__(name, email, password)
        self.__seller_id= id
        self.__address = address
        self.__address2 = address2
        self.__city = city
        self.__postal_code = postal_code
        self.__earned = {}
      
    def get_seller_id(self):
        return self.__seller_id
      
    def get_address(self):
        return self.__address
    
    def get_address2(self):
        return self.__address2

    def get_city(self):
        return self.__city

    def get_postal_code(self):
        return self.__postal_code
    
    def get_earned(self):
        return self.__earned
    

    def set_seller_id(self,seller_id):
        self.__seller_id = seller_id

    def set_address(self, address):
        self.__address = address
        
    def set_address2(self, address2):
        self.__address2 = address2

    def set_city(self, city):
        self.__city = city
        
    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code
        
    def set_earned(self, earned):
        self.__earned = earned
        

