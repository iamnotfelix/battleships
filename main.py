

from ui.ui import UI

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

ui = UI(player_logic, computer_logic, input_validator)
ui.start()


# todo: show a message with the player that won
# todo: implement a strategy for the computer
# todo: play a game to finish to see if it works properly
# todo: refactor the ui so it is more organized
# todo: add documentation to all non-ui functions (after everything is done)
