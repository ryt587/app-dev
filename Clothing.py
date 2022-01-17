import Products as p

class Clothing(p.Clothing):
    def __init__(self, colour, size):
    super().__init__(self, product_stock, product_image)
    self.__colour = colour
    self.__size = size

    def get_colour(self):
        return self.__colour

    def get_size(self):
        return self.__size


    def set_colour(self, self.__colour):
        self.__colour = colour

    def set_size(self, self.__size):
        self.__size = size
