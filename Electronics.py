import Products as p

class Electronics(p.Products):
    def __init__(self, gpu, cpu, storage, memory, size):
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


    def set_gpu(self.__gpu):
        self.__gpu = gpu

    def set_cpu(self.__gpu):
        self.__cpu = cpu

    def set_storage(self.__gpu):
        self.__storage = storage

    def set_memory(self.__gpu):
        self.__memory = memory

    def set_size(self.__gpu):
        self.__size = size

        
