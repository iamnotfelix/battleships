
from logic.logic import Logic


class ComputerLogic(Logic):

    def __init__(self, board, shots_board, position_validator):
        super().__init__(board, shots_board, position_validator)
