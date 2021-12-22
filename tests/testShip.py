
import unittest

from domain.position import Position
from domain.ship import Ship
from domain.orientation import Orientation


class ShipTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_properties(self):
        position = Position(1, 2, 3, Orientation.Vertical)
        ship = Ship(0, position)

        self.assertEqual(ship.id, 0)
        self.assertEqual(ship.position, position)
        self.assertEqual(ship.cells, ['ok1', 'ok2', 'ok3'])
