import User as u

class Seller(u.User):
  
  def __init__(self, email, password, address, city, postal_code):
      super().__init__(email, password)
      self.__address = address
      self.__city = city
      self.postal_code = postal_code
      
  def get_address(self):
      return self.__address
   
  def get_city(self):
      return self.__city
  
  def get_postal_code(self):
      return self.__postal_code
  
  
  def set_address(self, address):
      self.__address = address
    
  def set_city(self, city):
      self.__city = city
      
  def set_postal_code(self, postal_code):
      self.__postal_code = postal_code
      
 
