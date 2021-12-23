
import unittest

from logic.computerLogic import ComputerLogic
from boards.board import Board
from validation.validation import PositionValidation
from domain.position import Position


class ComputerLogicTest(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board()
        self.shots_board = Board()
        self.validator = PositionValidation()
        self.logic = ComputerLogic(self.board, self.shots_board, self.validator)

    def test_generate_position(self):
        position = self.logic.generate_position()
        self.assertTrue(isinstance(position, Position))

    def test_init_board(self):
        self.logic.init_board()
        self.assertEqual(len(self.logic.board.ships), 5)
