

class Ship:

    def __init__(self, ship_id, position):
        self.__id = ship_id
        self.__position = position
        self.__cells = [f"ok{i}" for i in range(1, self.__position.size + 1)]

    @property
    def id(self):
        return self.__id

    @property
    def position(self):
        return self.__position

    @property
    def cells(self):
        return self.__cells
