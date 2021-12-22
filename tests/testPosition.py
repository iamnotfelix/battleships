
import unittest
from domain.position import Position
from domain.orientation import Orientation


class PositionTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_properties(self):
        position = Position(1, 2, 3, Orientation.Vertical)
        self.assertEqual(position.x, 1)
        self.assertEqual(position.y, 2)
        self.assertEqual(position.size, 3)
        self.assertEqual(position.orientation, Orientation.Vertical)

        position = Position(2, 3, 4, Orientation.Horizontal)
        self.assertEqual(position.x, 2)
        self.assertEqual(position.y, 3)
        self.assertEqual(position.size, 4)
        self.assertEqual(position.orientation, Orientation.Horizontal)
