import shelve

class Product():

   def __init__(self, name, product_stock, product_image, created_product, price):
      db = shelve.open('user.db', 'c')
      users_dict={}
      try:
         if 'Products' in db:
               users_dict=db['Products']
         else:
               db['Products']=users_dict
         if users_dict=={}:
               id=1
         else:
               id=1
               while id in users_dict:
                  id+=1
      except:
         print("Error in retrieving Products from product.db.")
      db.close()
      self.__product_id = id
      self.__name = name
      self.__product_stock = product_stock
      self.__product_image = product_image
      self.__created_product = created_product
      self.__price = price
      self.__active = True
      self.__impression = 0
      self.__sold = 0

   def get_name(self):
      return self.__name
   
   def get_product_id(self):
      return self.__product_id

   def get_product_stock(self):
      return self.__product_stock

   def get_product_image(self):
      return self.__product_image
   
   def get_created_product(self):
      return self.__created_product
   
   def get_price(self):
      return self.__price
   
   def get_active(self):
      return self.__active
   
   def get_impression(self):
      return self.__impression
   
   def get_sold(self):
      return self.__sold


   def set_product_id(self, product_id):
      self.__product_id = product_id
      
   def set_name(self, name):
      self.__name = name

   def set_product_stock(self, product_stock):
      self.__product_stock = product_stock

   def set_product_image(self, product_image):
      self.__product_image = product_image

   def set_created_product(self, created_product):
      self.__created_product = created_product
      
   def set_price(self, price):
      self.__price = price
      
   def set_active(self, active):
      self.__active = active
      
   def set_impression(self, impression):
      self.__impression = impression
      
   def set_sold(self, sold):
      self.__sold = sold