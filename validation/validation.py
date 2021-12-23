
from domain.orientation import Orientation
from exceptions.exceptions import PositionException


class PositionValidation:

    def __init__(self):
        pass

    @staticmethod
    def __validate_bounds(x, y, size, orientation):
        if orientation == Orientation.Vertical:
            if x + size - 1 > 10:
                raise PositionException("The ship does not fit there! Ship out of bounds!")
        if orientation == Orientation.Horizontal:
            if y + size - 1 > 10:
                raise PositionException("The ship does not fit there! Ship out of bounds!")

    @staticmethod
    def __validate_overlapping(x, y, size, orientation, board):
        for i in range(1, size + 1):
            cell = board.board[x][y]
            if cell != '-':
                raise PositionException("Ships can not overlap!")
            if orientation == Orientation.Vertical:
                x += 1
            else:
                y += 1

    def validate(self, ship, board):
        x = ship.position.x
        y = ship.position.y
        size = ship.position.size
        orientation = ship.position.orientation

        self.__validate_bounds(x, y, size, orientation)
        self.__validate_overlapping(x, y, size, orientation, board)
