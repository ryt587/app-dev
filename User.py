from uuid import uuid4
import shelve

class User:
    id=uuid4().hex
    
    try:
        db = shelve.open('user.db', 'r')
        try:
            users_dict = db['Users']
            while id in users_dict:
                id=uuid4().hex
        except:
            print("Error in retrieving Users from user.db.")
        db.close()
    except:
        print("Error in retrieving Users from user.db.") 
    
    
            
    def __init__(self, email, password):
        self.__user_id=User.id
        self.__email=email
        self.__password=password
    
    def get_user_id(self):
        return self.__user_id
      
    def get_email(self):
        return self.__email
      
    def get_password(self):
        return self.__password

    def set_user_id(self, user_id):
        self.__user_id = user_id
    
    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password
