
import random

from logic.logic import Logic
from domain.position import Position
from domain.orientation import Orientation


class ComputerLogic(Logic):

    def __init__(self, board, shots_board, position_validator):
        super().__init__(board, shots_board, position_validator)

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


# if __name__ == "__main__":
#     from boards.board import Board
#     from validation.validation import PositionValidation
#     board = Board()
#     shots_board = Board()
#     validator = PositionValidation()
#     logic = ComputerLogic(board, shots_board, validator)
#     logic.init_board()
