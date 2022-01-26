from Figures.Figures import Figure
from Additional_stuff import *

class Rook(Figure):
    """Фигура Ладья"""

    def __init__(self, check_index, colour, chessboard):
        self.__firstMove = True
        self.__kingCommandToCastle = False
        super().__init__(check_index, "rook.png", colour, "Rook", chessboard)

    @possible_move_decorator
    def check_for_all_possible_moves(self):
        """Проверяет все возможные ходы Ладьи"""
        indexes_of_possible_moves = []
        for check_index in range(len(self.chessboard.get_checks)):
            if ((check_index - self.current_check_index) % 8 == 0 or
                    (check_index // 8 == self.current_check_index // 8)):
                indexes_of_possible_moves.append(check_index)

        # if self.name == "Rook" and self.kingCommandToCastle and self.firstMove:
        #     if self.current_check_index % 8 == 0:
        #         indexes_of_possible_moves.append(self.current_check_index + 3)
        #     if self.current_check_index % 8 == 7:
        #         indexes_of_possible_moves.append(self.current_check_index - 2)
        #     self.kingCommandToCastle = False
        return indexes_of_possible_moves

    def move_to(self, next_check_index):
        if self.name == "Rook" and self.kingCommandToCastle:
            self.write_down_move_and_die(next_check_index)
            self.current_check_index = next_check_index
            print(self.current_check_index)
        else:
            super(Rook, self).move_to(next_check_index)
        self.firstMove = False

    @property
    def firstMove(self):
        """Имеет фигуру или нет"""
        return self.__firstMove

    @firstMove.setter
    def firstMove(self, firstMove):
        """Сеттер hasFigure"""
        self.__firstMove = firstMove

    @property
    def kingCommandToCastle(self):
        return self.__kingCommandToCastle

    @kingCommandToCastle.setter
    def kingCommandToCastle(self, kingCommandToCastle):
        """Сеттер kingCommandToCastle"""
        self.__kingCommandToCastle = kingCommandToCastle
