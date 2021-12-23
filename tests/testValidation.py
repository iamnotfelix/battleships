
import unittest

from validation.validation import PositionValidation, InputValidation
from exceptions.exceptions import PositionException, InputException
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


class TestInputValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.validator = InputValidation()

    def test_validate_coordinate(self):
        with self.assertRaises(InputException) as ex:
            self.validator.validate_coordinate('b')
        self.assertEqual(str(ex.exception), "Coordinate must be a natural number!")

        with self.assertRaises(InputException) as ex:
            self.validator.validate_coordinate('0')
        self.assertEqual(str(ex.exception), "Coordinate out of bounds! Coordinates must be between 1 and 10!")

        with self.assertRaises(InputException) as ex:
            self.validator.validate_coordinate('11')
        self.assertEqual(str(ex.exception), "Coordinate out of bounds! Coordinates must be between 1 and 10!")

        coord = self.validator.validate_coordinate('10')
        self.assertEqual(coord, 10)

        coord = self.validator.validate_coordinate('1')
        self.assertEqual(coord, 1)

    def test_validate_orientation(self):
        with self.assertRaises(InputException) as ex:
            self.validator.validate_orientation('b')
        self.assertEqual(str(ex.exception), "Orientation must be 1 or 2!")

        with self.assertRaises(InputException) as ex:
            self.validator.validate_orientation('3')
        self.assertEqual(str(ex.exception), "Orientation must be 1 or 2!")

        with self.assertRaises(InputException) as ex:
            self.validator.validate_orientation('0')
        self.assertEqual(str(ex.exception), "Orientation must be 1 or 2!")

        orientation = self.validator.validate_orientation('1')
        self.assertEqual(orientation, Orientation.Vertical)

        orientation = self.validator.validate_orientation('2')
        self.assertEqual(orientation, Orientation.Horizontal)
