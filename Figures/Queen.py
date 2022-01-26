from Figures.Bishop import Bishop
from Figures.Figures import Figure
from Figures.Rook import Rook


class Queen(Rook, Bishop):  # Наследует паттерн движения от ферзя и слона
    """Ферзь"""

    def __init__(self, check_index, colour, chessboard):
        Figure.__init__(self, check_index, "queen.png", colour, "Queen", chessboard)

    def check_for_all_possible_moves(self):
        """Проверяет все возможные ходы Ферзя"""
        indexes_of_possible_moves = []
        for bishop_moves in Bishop.check_for_all_possible_moves(self):
            indexes_of_possible_moves.append(bishop_moves)

        for rook_moves in Rook.check_for_all_possible_moves(self):
            if rook_moves not in indexes_of_possible_moves:
                indexes_of_possible_moves.append(rook_moves)

        return indexes_of_possible_moves