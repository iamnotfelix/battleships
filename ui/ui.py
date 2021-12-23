
from domain.position import Position
from exceptions.exceptions import InputException, PositionException


class UI:

    def __init__(self, player_logic, input_validator):  # , player_board, player_record, computer_board, computer_record, validation
        self.__player_logic = player_logic
        self.__input_validator = input_validator

    @staticmethod
    def __display_game_rules():
        print("\nBattleship rules:\n"
              "The game is played on four grids, two for each player.\n"
              "The grids are 10X10 - and the individual squares in the grid are identified by letter and number.\n"
              "On one grid the player arranges ships and records the shots by the opponent.\n"
              "On the other grid the player records their own shots.\n"
              "Before play begins, each player secretly arranges their ships on their primary grid.\n"
              "Each ship occupies a number of consecutive squares on the grid, "
              "arranged either horizontally or vertically.\n"
              "The number of squares for each ship is determined by the type of the ship:\n"
              "\tNo.  Class       Size\n"
              "\t1.   Carrier     5\n"
              "\t2.   Battleship  4\n"
              "\t3.   Cruiser     3\n"
              "\t4.   Submarine   3\n"
              "\t5.   Destroyer   2\n"
              "The ships cannot overlap (i.e. only one ship can occupy any given square in the grid).\n"
              "The types and numbers of ships allowed are the same for each player.\n"
              "After the ships have been positioned, the game proceeds in a series of rounds.\n"
              "In each round, each player takes a turn to announce a target square in the opponent's "
              "grid which is to be shot at.\n"
              "The opponent announces whether or not the square is occupied by a ship.\n"
              "If it is a hit, the player who is hit marks this on their own grid.\n"
              "The attacking player marks the hit or miss on their own tracking or target grid "
              "in order to build up a picture of the opponent's fleet.\n"
              "When all of the squares of a ship have been hit, the ship's owner announces the sinking.\n"
              "If all of a player's ships have been sunk, the game is over and their opponent wins.\n"
              "If all ships of both players are sunk by the end of the round, the game is a draw.\n")

    @staticmethod
    def __display_menu():
        print("\nMenu:")
        print("rules\tDisplay Battleship rules.")
        print("play\tStart the game.")
        print("help\tDisplay this menu.")
        print("exit\tExit the game.")
        print("\nEnter command:")

    def __display_board(self):
        print(str(self.__player_logic.board))

    @staticmethod
    def __get_input(message, validator):
        while True:
            try:
                data = input(message)
                data = validator(data)
                break
            except InputException as ex:
                print(str(ex))
        return data

    def __get_ship_position(self, ship):
        print(f"Position your {ship['type']} of size {ship['size']}")
        row = self.__get_input("Row: ", self.__input_validator.validate_coordinate)
        col = self.__get_input("Col: ", self.__input_validator.validate_coordinate)

        print("Chose a valid orientation:\nvertical - 1 or horizontal - 2")
        orientation = self.__get_input("Orientation: ", self.__input_validator.validate_orientation)

        position = Position(row, col, ship['size'], orientation)
        return position

    def __get_hit_position(self):
        pass

    @staticmethod
    def __get_command():
        command = input(">>>")
        command = command.strip()
        return command

    def __menu_handler(self):
        self.__display_menu()
        while True:
            command = self.__get_command()
            try:
                if command == "exit":
                    exit()
                elif command == "help":
                    self.__display_menu()
                elif command == "rules":
                    self.__display_game_rules()
                elif command == "play":
                    self.__start_game()
                else:
                    raise Exception("Invalid command!")
            except Exception as ex:
                print(str(ex))

    def __start_game(self):
        print("Step 1 - Place your ships on the board.")
        ships = [
            {
                "type": "Carrier",
                "size": 5
            },
            {
                "type": "Battleship",
                "size": 4
            },
            {
                "type": "Cruiser",
                "size": 3
            },
            {
                "type": "Submarine",
                "size": 3
            },
            {
                "type": "Destroyer",
                "size": 2
            }
        ]
        for ship in ships:
            while True:
                try:
                    self.__display_board()
                    position = self.__get_ship_position(ship)
                    self.__player_logic.add_ship(position)
                    break
                except PositionException as ex:
                    print(str(ex))
        print("\nYour final board: ")
        self.__display_board()

    def start(self):
        self.__menu_handler()
