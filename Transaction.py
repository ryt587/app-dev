import datetime as d
from uuid import uuid4


class Transaction(): 
        
    def __init__(self, product_list):
        self.__id=uuid4().hex
        self.__product_list=product_list
        self.__status=1
        self.__transaction_date=d.date.today().strftime("%Y-%m-%d")
        self.__expected_date=d.date.today().strftime("%Y-%m-%d")+ d.timedelta(15)
        self.__delivered_date=0
      
    def get_id(self):
        return self.__id
    
    def get_product_list(self):
        return self.__product_list
    
    def get_status(self):
        return self.__status
    
    def get_transaction_date(self):
        return self.__transaction_date
    
    def get_expected_date(self):
        return self.__expected_date
    
    def get_delivered_date(self):
        return self.__delivered_date
    
    def set_id(self, id):
        self.__id = id
    
    def set_product_list(self, product_list):
        self.__product_list = product_list
        
    def set_status(self, status):
        self.__status = status
    
    def set_transaction_date(self, transaction_date):
        self.__transaction_date = transaction_date
        
    def set_expected_date(self,expected_date):
        self.__expected_date = expected_date

    def set_delivered_date(self,delivered_date):
        self.__delivered_date = delivered_date