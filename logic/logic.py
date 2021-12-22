

class Logic:

    def __init__(self, board, position_validator):
        self.__board = board
        self.__position_validator = position_validator
        self.__id_counter = -1

    def id(self):
        self.__id_counter += 1
        return self.__id_counter

    # todo: create auto ids for ships
    def add_ship(self, position):
        ship = self.__board.create_ship(self.id(), position)
        self.__position_validator.validate(ship)
        self.__board.add_ship(ship)
