import shelve
class Refund():
    def __init__(self, product_name, reason):
        db = shelve.open('user.db', 'c')
        refund_dict={}
        try:
            if 'Refunds' in db:
                refund_dict=db['Refunds']
            else:
                db['Refunds']=refund_dict
            if refund_dict=={}:
                id=1
            else:
                id=1
                while id in refund_dict:
                    id+=1
        except:
            print("Error in retrieving Products from product.db.")
        db.close()
        self.__id=id
        self.__product_name=product_name
        self.__reason=reason
        
    def get_id(self):
        return self.__id
    
    def get_product_name(self):
        return self.__product_name
    
    def get_reason(self):
        return self.__reason
    
    def set_id(self, id):
      self.__id = id
      
    def set_product_name(self, product_name):
      self.__product_name= product_name
      
    def set_reason(self, reason):
      self.__reason = reason