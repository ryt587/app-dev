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
      
   def __init__(self, product_stock, product_image):
      self.__product_id = Product.id
      self.__product_stock = product_stock
      self.__product_image = product_image
   
   def get_product_id(self):
      return self.__product_id
     
   def get_product_stock(self):
      return self.__product_stock
    
   def get_product_image(self):
      return self.__product_image
   
   
   def set_product_id(self, product_id):
      self.__product_id = product_id
      
   def set_product_stock(self, product_stock):
      self.__product_stock = product_stock
      
   def set_product_image(self, product_image):
      self.__product_image = product_image
      
