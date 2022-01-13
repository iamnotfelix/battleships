

from ui.ui import UI
from gui.gui import GUI

from boards.board import Board
from logic.logic import Logic
from logic.computerLogic import ComputerLogic
from validation.validation import PositionValidation, InputValidation

position_validator = PositionValidation()
input_validator = InputValidation()

player_board = Board()
player_shots_board = Board()
player_logic = Logic(player_board, player_shots_board, position_validator)

computer_board = Board()
computer_shots_board = Board()
computer_logic = ComputerLogic(computer_board, computer_shots_board, position_validator)
computer_logic.init_board()

print("Menu:")
print("console\t\tFor console game.")
print("gui\t\tFor GUI game.")
print("exit\t\tTo exit.")
print("Enter a command:")

while True:

    command = input(">>>")
    command = command.strip()
    if command == "exit":
        exit()
    elif command == "console":
        ui = UI(player_logic, computer_logic, input_validator)
        ui.start()
    elif command == "gui":
        gui = GUI()
        gui.start()
    else:
        print("Invalid command!")

# todo: add documentation to all non-ui functions (after everything is done)
