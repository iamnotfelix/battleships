

class Ship:

    def __init__(self, ship_id, position):
        self.__id = ship_id
        self.__position = position
        self.__cells = [False for i in range(0, self.__position.size)]

    def __len__(self):
        return len(self.__cells)

    def __getitem__(self, item):
        return self.__cells[item]

    def __setitem__(self, key, value):
        self.__cells[key] = value

    @property
    def id(self):
        return self.__id

    @property
    def position(self):
        return self.__position

    def check_ship(self):
        destroyed = True
        for cell in self.__cells:
            if not cell:
                destroyed = False
        return destroyed

# todo: len, getitem, setitem - might be useless now (delete them?)
