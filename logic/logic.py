

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

    def get_boards(self):
        # t_l_corner = "┌"
        # t_r_corner = "┐"
        # b_l_corner = "└"
        # b_r_corner = "┘"
        # cross = "┼"
        # horizontal = "─"
        # vertical = "│"
        # b_edge = "┴"
        # l_edge = "┤"
        # t_edge = "┬"
        # r_edge = "├"
        panel = '\tYour board\t\t\tYour shots\n'
        panel += '  '
        for i in range(1, 11):
            panel += f'{i} '
        panel += '\t\t   '
        for i in range(1, 11):
            panel += f'{i} '
        panel += '\n'

        for i in range(1, 11):
            if i == 10:
                panel += f'{i} '
            else:
                panel += f'{i}  '
            for j in range(1, 11):
                cell = self._board.board[i][j]
                if isinstance(cell, dict):
                    panel += f'{cell["id"]} '
                else:
                    panel += f'{cell} '

            panel += '\t\t'
            if i == 10:
                panel += f'{i} '
            else:
                panel += f'{i}  '
            for j in range(1, 11):
                cell = self._shots_board.board[i][j]
                if isinstance(cell, dict):
                    panel += f'{cell["id"]} '
                else:
                    panel += f'{cell} '
            panel += '\n'
        return panel

    def id(self):
        self._id_counter += 1
        return self._id_counter

    def add_ship(self, position):
        ship = self._board.create_ship(self.id(), position)
        self._position_validator.validate(ship, self._board)
        self._board.add_ship(ship)

    def record_hit(self, position):
        self._shots_board.add_hit(position)

    def add_hit(self, position):
        is_hit, is_destroyed = self._board.add_hit(position)
        return is_hit, is_destroyed

    def is_game_over(self):
        ships = self._board.ships
        game_over = True
        for key in ships.keys():
            ship = ships[key]
            if not ship.is_destroyed():
                game_over = False
        return game_over
