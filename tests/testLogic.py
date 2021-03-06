
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

    def test_get_boards(self):
        self.logic.add_ship(Position(1, 2, 3, Orientation.Vertical))
        boards = self.logic.get_boards()
        self.assertNotEqual(len(boards), 0)

    def test_add_ship(self):
        position = Position(1, 2, 3, Orientation.Vertical)
        self.logic.add_ship(position)
        self.assertEqual(self.board.ships.__len__(), 1)

    def test_record_hit(self):
        self.logic.record_hit(Position(1, 1))
        self.assertEqual(self.logic.shots_board.board[1][1], 'X')

    def test_add_hit(self):
        is_hit, is_destroyed = self.logic.add_hit(Position(1, 2))
        self.assertEqual(is_hit, False)
        self.assertEqual(is_destroyed, False)

        self.logic.add_ship(Position(1, 2, 3, Orientation.Vertical))
        is_hit, is_destroyed = self.logic.add_hit(Position(1, 2))
        self.assertEqual(is_hit, True)
        self.assertEqual(is_destroyed, False)

    def test_is_game_over(self):
        self.logic.add_ship(Position(1, 2, 2, Orientation.Horizontal))
        self.assertFalse(self.logic.is_game_over())

        self.logic.add_hit(Position(1, 2))
        self.assertFalse(self.logic.is_game_over())

        self.logic.add_hit(Position(1, 3))
        self.assertTrue(self.logic.is_game_over())
