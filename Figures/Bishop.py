from Figures.Figures import Figure
from Additional_stuff import *

class Bishop(Figure):
    """Фигура Слон"""

    def __init__(self, check_index, colour, chessboard):
        super().__init__(check_index, "bishop.png", colour, "Bishop", chessboard)

    @possible_move_decorator
    def check_for_all_possible_moves(self):
        """Проверяет все возможные ходы Слона"""
        indexes_of_possible_moves = []
        for check_index in range(len(self.chessboard.get_checks)):
            if (((check_index - self.current_check_index) % 7 == 0 or
                 (check_index - self.current_check_index) % 9 == 0) and
                    self.chessboard.get_check(self.current_check_index).color == self.chessboard.get_check(
                        check_index).color):
                indexes_of_possible_moves.append(check_index)
        return indexes_of_possible_moves