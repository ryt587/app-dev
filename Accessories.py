import Products as p

class Accessories(p.Product):
    def __init__(self, name, product_stock, product_image, created_product, price, colour, size, accessory_type):
        super().__init__(name, product_stock, product_image, created_product, price)
        self.__colour = colour
        self.__size = size
        self.__accessory_type = accessory_type

    def get_colour(self):
        return self.__colour

    def get_size(self):
        return self.__size

    def get_accessory_type(self):
        return self.get_accessory_type()

    def set_colour(self, colour):
        self.__colour = colour

    def set_size(self, size):
        self.__size = size

    def set_accessory_type(self, product_type):
        self.__accessory_type = accessory_type
