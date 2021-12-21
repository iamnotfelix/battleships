

class Ship:

    def __init__(self, id, size, orientation, position):
        self.__id = id
        self.__size = size
        self.__orientation = orientation
        self.__position = position

    @property
    def id(self):
        return self.__id

    @property
    def size(self):
        return self.__size

    @property
    def orientation(self):
        return self.__orientation

    @property
    def position(self):
        return self.__position
