
import unittest

from domain.position import Position
from domain.ship import Ship
from domain.orientation import Orientation


class ShipTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_len(self):
        ship = Ship(0, Position(1, 2, 3, Orientation.Vertical))
        self.assertEqual(len(ship), 3)

    def test_getitem(self):
        ship = Ship(0, Position(1, 2, 3, Orientation.Vertical))
        self.assertEqual(ship[0], False)
        self.assertEqual(ship[1], False)
        self.assertEqual(ship[2], False)

    def test_setitem(self):
        ship = Ship(0, Position(1, 2, 3, Orientation.Vertical))
        ship[0] = True
        ship[2] = True
        self.assertEqual(ship[0], True)
        self.assertEqual(ship[1], False)
        self.assertEqual(ship[2], True)

    def test_properties(self):
        position = Position(1, 2, 3, Orientation.Vertical)
        ship = Ship(0, position)

        self.assertEqual(ship.id, 0)
        self.assertEqual(ship.position, position)

    def test_is_destroyed(self):
        ship = Ship(0, Position(1, 2, 3, Orientation.Vertical))

        self.assertFalse(ship.is_destroyed())
