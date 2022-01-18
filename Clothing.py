import Products as p

class Clothing(p.Product):
    def __init__(self, name, product_stock, product_image, colour, size):
        super().__init__(name, product_stock, product_image)
        self.__colour = colour
        self.__size = size

    def get_colour(self):
        return self.__colour

    def get_size(self):
        return self.__size


    def set_colour(self, colour):
        self.__colour = colour

    def set_size(self, size):
        self.__size = size
