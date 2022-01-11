from uuid import uuid4
import shelve

class Product():
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
      
   def __init__(self, product_size, product_type, product_category, product_stock):
      self.__product_id = Product.id
      self.__product_size = product_size
      self.__product_type = product_type
      self.__product_category = product_category
      self.__product_stock = product_stock
   
   def get_product_id(self):
      return self.__product_id
      
   def get_product_size(self):
      return self.__product_size
  
   def get_product_type(self):
      return self.__product_type
  
   def get_product_category(self):
      return self.__product_category
     
   def get_product_stock(self):
      return self.__product_stock
    
   
   
   def set_product_id(self, product_id):
      self.__product_id = product_id
    
   def set_product_size(self, product_size):
      self.__product_size = product_size
      
   def set_product_type(self, product_type):
      self.__product_type = product_type
      
   def set_product_category(self, product_category):
      self.__product_category = product_category
      
   def set_product_stock(self, product_stock):
      self.__product_stock = product_stock
      
