
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

        for i in range(1, size + 1):
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
        pass


if __name__ == "__main__":
    board = Board()
    board.add_ship(Ship(0, Position(1, 1, 3, Orientation.Vertical)))
    board.add_ship(Ship(1, Position(2, 6, 4, Orientation.Vertical)))
    board.add_ship(Ship(2, Position(7, 2, 5, Orientation.Horizontal)))
    board.add_ship(Ship(3, Position(10, 8, 3, Orientation.Horizontal)))
    board.add_ship(Ship(4, Position(1, 9, 2, Orientation.Vertical)))
    print(str(board))
