
from domain.ship import Ship
from domain.orientation import Orientation
from domain.position import Position


class Board:

    def __init__(self):
        self.__board = [['-' for i in range(0, 11)] for j in range(0, 11)]
        self.__ships = dict()

    def __str__(self):
        matrix = ""
        for i in range(1, len(self.__board)):
            row = self.__board[i]
            for j in range(1, len(row)):
                cell = row[j]
                if cell == '-':
                    matrix += str(cell) + " "
                else:
                    matrix += str(cell['id']) + " "
            matrix += "\n"
        return matrix

    @property
    def board(self):
        return self.__board

    @property
    def ships(self):
        return self.__ships

    @staticmethod
    def create_ship(ship_id, position):
        return Ship(ship_id, position)

    def __add_ship_to_matrix(self, ship):
        x = ship.position.x
        y = ship.position.y
        size = ship.position.size
        orientation = ship.position.orientation

        for i in range(0, size):
            cell = {
                "id": ship.id,
                "cell": i
            }
            self.__board[x][y] = cell
            if orientation == Orientation.Vertical:
                x += 1
            else:
                y += 1

    def add_ship(self, ship):
        self.__ships[ship.id] = ship
        self.__add_ship_to_matrix(ship)

    def check_ship(self, ship_id):
        ship = self.__ships[ship_id]
        destroyed = True
        for i in range(0, len(ship)):
            if not ship[i]:
                destroyed = False
        return destroyed

    def add_hit(self, position):
        x = position.x
        y = position.y

        cell = self.__board[x][y]
        self.__board[x][y] = 'X'

        if isinstance(cell, dict):
            hit_ship_id = cell["id"]
            hit_ship_cell = cell["cell"]
            hit_ship = self.__ships[hit_ship_id]
            hit_ship[hit_ship_cell] = True
            return True, self.check_ship(hit_ship_id)
        return False, False

    def debug_init(self):
        self.add_ship(Ship(0, Position(1, 1, 3, Orientation.Vertical)))
        self.add_ship(Ship(1, Position(2, 6, 4, Orientation.Vertical)))
        self.add_ship(Ship(2, Position(7, 2, 5, Orientation.Horizontal)))
        self.add_ship(Ship(3, Position(10, 8, 3, Orientation.Horizontal)))
        self.add_ship(Ship(4, Position(1, 9, 2, Orientation.Vertical)))

