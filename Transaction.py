from datetime import date
from uuid import uuid4


class Transaction: 
        
    def __init__(self, product_list):
        self.__id=uuid4().hex
        self.__product_list=product_list
        self.__status='Delivery not collected'
        self.__transaction_date=date.today().strftime("%Y-%m-%d")
        self.__refund=True
      
    def get_id(self):
        return self.__id
    
    def get_product_list(self):
        return self.__product_list
    
    def get_status(self):
        return self.__status
    
    def get_transaction_date(self):
        return self.__transaction_date
    
    def get_refund(self):
        return self.__refund
    
    def set_id(self, id):
        self.__id = id
    
    def set_product_list(self, product_list):
        self.__product_list = product_list
        
    def set_status(self, status):
        self.__status = status
    
    def set_transaction_date(self, transaction_date):
        self.__transaction_date = transaction_date
        
    def set_refund(self, refund):
        self.__refund = refund
