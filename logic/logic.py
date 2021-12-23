

class Logic:

    def __init__(self, board, shots_board, position_validator):
        self._board = board
        self._shots_board = shots_board
        self._position_validator = position_validator
        self._id_counter = -1

    @property
    def board(self):
        return self._board

    @property
    def shots_board(self):
        return self._shots_board

    def id(self):
        self._id_counter += 1
        return self._id_counter

    def add_ship(self, position):
        ship = self._board.create_ship(self.id(), position)
        self._position_validator.validate(ship, self._board)
        self._board.add_ship(ship)

    def add_hit(self, position):
        is_hit, is_destroyed = self._board.add_hit(position)
        self._shots_board.add_hit(position)
        return is_hit, is_destroyed

    def is_game_over(self):
        ships = self._board.ships
        game_over = True
        for key in ships.keys():
            ship = ships[key]
            if not ship.is_destroyed():
                game_over = False
        return game_over



