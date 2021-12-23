

from ui.ui import UI

from boards.board import Board
from logic.logic import Logic
from validation.validation import PositionValidation, InputValidation

position_validator = PositionValidation()
input_validator = InputValidation()

player_board = Board()
shots_board = Board()
player_logic = Logic(player_board, shots_board, position_validator)

ui = UI(player_logic, input_validator)
ui.start()
