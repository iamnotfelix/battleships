

class Position:

    def __init__(self, x, y, size=None, orientation=None):
        self.__x = x
        self.__y = y
        self.__size = size
        self.__orientation = orientation

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def size(self):
        return self.__size

    @property
    def orientation(self):
        return self.__orientation
