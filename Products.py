class Product():
  
   def __init__(self, product_size, product_type, product_category, product_stock):
      self.__product_size = product_size
      self.__product_type = product_type
      self.__product_category = product_category
      self.__product_stock = product_stock
      
   def get_product_size(self):
      return self.__product_size
  
   def get_product_type(self):
      return self.__product_type
  
   def get_product_category(self):
      return self.__product_category
     
   def get_product_stock(self):
      return self.__product_stock
    
    
    
   def set_product_size(self, product_size):
      self.__product_size = product_size
      
   def set_product_type(self, product_type):
      self.__product_type = product_type
      
   def set_product_category(self, product_category):
      self.__product_category = product_category
      
   def set_product_stock(self, product_stock):
      self.__product_stock = product_stock
      
