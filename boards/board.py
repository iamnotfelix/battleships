
from domain.ship import Ship
from domain.orientation import Orientation
from domain.position import Position


class Board:

    def __init__(self):
        self.__board = [['-' for i in range(0, 11)] for j in range(0, 11)]
        self.__ships = dict()

    def __str__(self):
        panel = ''
        panel += '  '
        for i in range(1, 11):
            panel += f'{i} '
        panel += '\n'

        for i in range(1, 11):
            if i == 10:
                panel += f'{i} '
            else:
                panel += f'{i}  '
            for j in range(1, 11):
                cell = self.__board[i][j]
                if isinstance(cell, dict):
                    panel += f'{cell["id"]} '
                else:
                    panel += f'{cell} '
            panel += '\n'

        return panel

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
            return True, hit_ship.is_destroyed()
        return False, False

    # to be deleted or commented after development
    def debug_init(self):
        self.add_ship(Ship(0, Position(1, 1, 3, Orientation.Vertical)))
        self.add_ship(Ship(1, Position(2, 6, 4, Orientation.Vertical)))
        self.add_ship(Ship(2, Position(7, 2, 5, Orientation.Horizontal)))
        self.add_ship(Ship(3, Position(10, 8, 3, Orientation.Horizontal)))
        self.add_ship(Ship(4, Position(1, 9, 2, Orientation.Vertical)))

