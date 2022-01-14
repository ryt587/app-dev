import shelve


class User: 
        
    def __init__(self, email, password):
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
                id=1
                while id in users_dict:
                    id+=1
        except:
            print("Error in retrieving Users from user.db.")
        db.close()
        self.__user_id=id
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
