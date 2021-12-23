

class Logic:

    def __init__(self, board, shots_board, position_validator):
        self.__board = board
        self.__shots_board = shots_board
        self.__position_validator = position_validator
        self.__id_counter = -1

    @property
    def board(self):
        return self.__board

    @property
    def shots_board(self):
        return self.__shots_board

    def id(self):
        self.__id_counter += 1
        return self.__id_counter

    def add_ship(self, position):
        ship = self.__board.create_ship(self.id(), position)
        self.__position_validator.validate(ship, self.__board)
        self.__board.add_ship(ship)

    def add_hit(self, position):
        is_hit, is_destroyed = self.__board.add_hit(position)
        self.__shots_board.add_hit(position)
        return is_hit, is_destroyed

    def is_game_over(self):
        ships = self.__board.ships
        game_over = True
        for key in ships.keys():
            ship = ships[key]
            if not ship.is_destroyed():
                game_over = False
        return game_over



