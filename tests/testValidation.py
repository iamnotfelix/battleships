
import unittest

from validation.validation import PositionValidation
from exceptions.exceptions import PositionException
from boards.board import Board
from domain.position import Position
from domain.orientation import Orientation
from domain.ship import Ship


class PositionValidationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board()
        self.validator = PositionValidation()

    def test_validate(self):
        self.board.add_ship(Ship(0, Position(1, 1, 3, Orientation.Vertical)))
        self.board.add_ship(Ship(1, Position(2, 6, 4, Orientation.Vertical)))
        self.board.add_ship(Ship(2, Position(7, 2, 5, Orientation.Horizontal)))
        self.board.add_ship(Ship(3, Position(10, 8, 3, Orientation.Horizontal)))
        self.board.add_ship(Ship(4, Position(1, 9, 2, Orientation.Vertical)))

        ship = Ship(5, Position(1, 1, 3, Orientation.Horizontal))
        with self.assertRaises(PositionException) as ex:
            self.validator.validate(ship, self.board)
        self.assertEqual(str(ex.exception), "Ships can not overlap!")

        ship = Ship(6, Position(1, 1, 3, Orientation.Vertical))
        with self.assertRaises(PositionException) as ex:
            self.validator.validate(ship, self.board)
        self.assertEqual(str(ex.exception), "Ships can not overlap!")

        ship = Ship(7, Position(5, 4, 4, Orientation.Horizontal))
        with self.assertRaises(PositionException) as ex:
            self.validator.validate(ship, self.board)
        self.assertEqual(str(ex.exception), "Ships can not overlap!")

        ship = Ship(8, Position(4, 2, 4, Orientation.Vertical))
        with self.assertRaises(PositionException) as ex:
            self.validator.validate(ship, self.board)
        self.assertEqual(str(ex.exception), "Ships can not overlap!")

        ship = Ship(9, Position(9, 8, 4, Orientation.Horizontal))
        with self.assertRaises(PositionException) as ex:
            self.validator.validate(ship, self.board)
        self.assertEqual(str(ex.exception), "The ship does not fit there! Ship out of bounds!")

        ship = Ship(10, Position(10, 3, 2, Orientation.Vertical))
        with self.assertRaises(PositionException) as ex:
            self.validator.validate(ship, self.board)
        self.assertEqual(str(ex.exception), "The ship does not fit there! Ship out of bounds!")
