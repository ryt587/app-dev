import shelve

class Product():

   def __init__(self, product_stock, product_image):
      db = shelve.open('product.db', 'c')
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
