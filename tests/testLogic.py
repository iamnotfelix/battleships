
import unittest

from boards.board import Board
from logic.logic import Logic
from validation.validation import PositionValidation
from domain.orientation import Orientation
from domain.position import Position


class LogicTest(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board()
        self.shots_board = Board()
        self.position_validation = PositionValidation()
        self.logic = Logic(self.board, self.shots_board, self.position_validation)

    def test_properties(self):
        self.assertEqual(self.logic.board, self.board)
        self.assertEqual(self.logic.shots_board, self.shots_board)

    def test_add_ship(self):
        position = Position(1, 2, 3, Orientation.Vertical)
        self.logic.add_ship(position)
        self.assertEqual(self.board.ships.__len__(), 1)
