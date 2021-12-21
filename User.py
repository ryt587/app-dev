class User:
    count_id=0

    def __init__(self, email, password):
        self.__class__.count_id+=1
        self.__user_id=self.__class__.count_id
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
