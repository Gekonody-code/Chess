from Figures.Figures import Figure
from Additional_stuff import *

class King(Figure):
    def __init__(self, check_index, colour, chessboard):
        self.firstMove = True
        super().__init__(check_index, "king.png", colour, "King", chessboard)

    @possible_move_decorator
    def check_for_all_possible_moves(self):
        indexes_of_possible_moves = []
        for i in range(3):
            if self.current_check_index // 8 != 7:
                if (self.current_check_index + 7 + i) // 8 == self.current_check_index // 8 + 1:
                    indexes_of_possible_moves.append(self.current_check_index + 7 + i)
            if self.current_check_index // 8 != 0:
                if (self.current_check_index - 7 - i) // 8 == self.current_check_index // 8 - 1:
                    indexes_of_possible_moves.append(self.current_check_index - 7 - i)
        if self.current_check_index % 8 != 0:
            indexes_of_possible_moves.append(self.current_check_index - 1)
        if self.current_check_index % 8 != 7:
            indexes_of_possible_moves.append(self.current_check_index + 1)

        indexes_of_possible_moves.append(self.current_check_index)

        if self.firstMove:
            indexes_for_castling = self.castling()
            indexes_of_possible_moves += indexes_for_castling

        return indexes_of_possible_moves

    def move_to(self, next_check_index):
        castling_signal = next_check_index in self.castling()
        previous_check_index = self.current_check_index
        super(King, self).move_to(next_check_index)

        if castling_signal:

            if next_check_index < previous_check_index:
                self.chessboard.get_check(next_check_index - 2).figure.kingCommandToCastle = True
                self.chessboard.get_check(next_check_index - 2).figure.move_to(next_check_index + 1)
            else:
                print("YA2")
                self.chessboard.get_check(next_check_index + 1).figure.kingCommandToCastle = True
                print(self.chessboard.get_check(next_check_index + 1).figure)
                self.chessboard.get_check(next_check_index + 1).figure.move_to(next_check_index - 1)

        if self.firstMove:
            self.firstMove = False

    def castling(self):
        rooks_indexes = [0, 7, 56, 63]
        rooks_for_castling = []
        for rooks_index in rooks_indexes:
            if self.chessboard.get_check(rooks_index).hasFigure and \
                    self.chessboard.get_check(rooks_index).figure.name == "Rook" and \
                    self.chessboard.get_check(rooks_index).figure.firstMove:

                if self.colour == "white" and rooks_index > 7:

                    if 61 in self.chessboard.get_check(rooks_index).figure.check_for_all_possible_moves() or \
                            59 in self.chessboard.get_check(rooks_index).figure.check_for_all_possible_moves():
                        rooks_for_castling.append(rooks_index)
                else:
                    if 3 in self.chessboard.get_check(rooks_index).figure.check_for_all_possible_moves() or \
                            5 in self.chessboard.get_check(rooks_index).figure.check_for_all_possible_moves():
                        rooks_for_castling.append(rooks_index)

        for i in range(len(rooks_for_castling)):
            if rooks_for_castling[i] < self.current_check_index:
                rooks_for_castling[i] += 2
            else:
                rooks_for_castling[i] -= 1

        return rooks_for_castling

        @property
        def firstMove(self):
            """Имеет фигуру или нет"""
            return self.__firstMove

        @firstMove.setter
        def firstMove(self, firstMove):
            """Сеттер hasFigure"""
            self.__firstMove = firstMove