import Products as p

class Electronics(p.Products):
    def __init__(self, name, product_stock, product_image, gpu, cpu, storage, memory, size):
        super().__init__(self, name, product_stock, product_image)
        self.__gpu = gpu
        self.__cpu = cpu
        self.__storage = storage
        self.__memory = memory
        self.__size = size

    def get_gpu(self):
        return self.__gpu

    def get_cpu(self):
        return self.__cpu

    def get_storage(self):
        return self.__storage

    def get_memory(self):
        return self.__memory

    def get_size(self):
        return self.__size


    def set_gpu(self, gpu):
        self.__gpu = gpu

    def set_cpu(self, cpu):
        self.__cpu = cpu

    def set_storage(self, storage):
        self.__storage = storage

    def set_memory(self, memory):
        self.__memory = memory

    def set_size(self, size):
        self.__size = size
