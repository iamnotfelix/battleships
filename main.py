

from ui.ui import UI

from boards.board import Board
from logic.logic import Logic
from validation.validation import PositionValidation

player_board = Board()
position_validator = PositionValidation()
player_logic = Logic(player_board, position_validator)

ui = UI(player_logic)
ui.start()
