
import unittest

from boards.board import Board

from domain.orientation import Orientation
from domain.position import Position
from domain.ship import Ship


class BoardTest(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board()

    def test_properties(self):
        mat = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]
        self.assertEqual(self.board.board, mat)
        self.assertEqual(self.board.ships, dict())

    def test_create_ship(self):
        ship = self.board.create_ship(1, Position(1, 2, 3, Orientation.Vertical))
        self.assertEqual(ship.id, 1)

    def test_add_ship(self):
        ship1 = self.board.create_ship(1, Position(1, 2, 3, Orientation.Vertical))
        self.board.add_ship(ship1)
        self.assertEqual(len(self.board.ships), 1)
        self.assertEqual(self.board.ships[1], ship1)
        # todo: verify somehow the matrix

        # ship2 = self.board.create_ship(1, Position(1, 2, 3, Orientation.Vertical))
        # ship3 = self.board.create_ship(1, Position(1, 2, 3, Orientation.Vertical))
