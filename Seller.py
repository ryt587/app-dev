import User as u

class Seller(u.User):
  
  def __init__(self, address, city, postal_code, email, password)
      super().__innit__(email, password)
      self.__address = address
      self.postal_code = postal_code
      self.__email = email
      self.__password = password
      
  def get_address(self):
      return self.__address
   
  def get_city(self):
      return self.__city
  
  def get_postal_code(self):
      return self.__postal
  
  
  def set_address(self, address):
      self.__address = address
    
  def set_city(self, city):
      self.__city = city
      
  def set_postal_code(self, postal_code):
      self.__postal_code = postal_code
      
 
