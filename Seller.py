import User as u
import shelve

class Seller(u.User):
  
    def __init__(self, name, email, password, address, city, postal_code):
        db = shelve.open('user.db', 'c')
        users_dict={}
        try:
            if 'Sellers' in db:
                users_dict=db['Sellers']
            else:
                db['Sellers']=users_dict
            if users_dict=={}:
                id=1
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
        self.__city = city
        self.postal_code = postal_code
      
    def get_seller_id(self):
        return self.__seller_id
      
    def get_address(self):
        return self.__address

    def get_city(self):
        return self.__city

    def get_postal_code(self):
        return self.__postal_code

    def set_seller_id(self,seller_id):
        self.__seller_id = seller_id

    def set_address(self, address):
        self.__address = address

    def set_city(self, city):
        self.__city = city
        
    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code
        

