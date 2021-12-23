
from domain.orientation import Orientation
from exceptions.exceptions import PositionException, InputException


class PositionValidation:

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


class InputValidation:

    @staticmethod
    def validate_coordinate(coord):
        try:
            coord = int(coord)
            if coord < 1 or coord > 10:
                raise InputException("Coordinate out of bounds! Coordinates must be between 1 and 10!")
        except ValueError:
            raise InputException("Coordinate must be a natural number!")
        return coord

    @staticmethod
    def validate_orientation(orientation):
        try:
            orientation = int(orientation)
            if orientation != 1 and orientation != 2:
                raise InputException("Orientation must be 1 or 2!")
            orientation = Orientation.Vertical if orientation == 1 else Orientation.Horizontal
        except ValueError:
            raise InputException("Orientation must be 1 or 2!")
        return orientation
