
import random

from logic.logic import Logic
from domain.position import Position
from domain.orientation import Orientation


class ComputerLogic(Logic):

    def __init__(self, board, shots_board, position_validator):
        super().__init__(board, shots_board, position_validator)
        self.__hit_queue = list()

    @staticmethod
    def generate_position(size=None, orientation=None):
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        size = random.randint(2, 5) if not size else size
        orientation = random.randint(1, 2) if not orientation else orientation
        orientation = Orientation.Vertical if orientation == 1 else Orientation.Horizontal
        position = Position(x, y, size, orientation)
        return position

    def init_board(self):
        sizes = [5, 4, 3, 3, 2]
        for size in sizes:
            while True:
                try:
                    position = self.generate_position(size)
                    self.add_ship(position)
                    break
                except Exception as ex:
                    pass

    def get_new_position(self):
        position = None
        if len(self.__hit_queue):
            pair = self.__hit_queue[0]
            position = Position(pair[0], pair[1])
            self.__hit_queue.pop(0)
        else:
            is_valid = False
            while not is_valid:
                position = self.generate_position()
                if self._shots_board.board[position.x][position.y] != 'X':
                    is_valid = True
        return position

    def record_hit(self, position, is_hit, is_destroyed):
        dir_x = [1, 0, -1, 0]
        dir_y = [0, 1, 0, -1]
        super().record_hit(position)
        if is_hit and not is_destroyed:
            x = position.x
            y = position.y
            for i in range(0, 4):
                new_x = x + dir_x[i]
                new_y = y + dir_y[i]
                if 1 <= new_x <= 10 and 1 <= new_y <= 10 and self._shots_board.board[new_x][new_y] != 'X':
                    self.__hit_queue.append((new_x, new_y))
