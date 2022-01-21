from Figures import Figure
import time
from Additional_stuff import *


class Rook(Figure):
    """Фигура Ладья"""

    def __init__(self, check_index, colour, chessboard):
        super().__init__(check_index, "rook.png", colour, "Rook", chessboard)

    @possible_move_decorator
    def check_for_all_possible_moves(self):
        """Проверяет все возможные ходы Ладьи"""
        indexes_of_possible_moves = []
        for check_index in range(len(self.chessboard.get_checks)):
            if ((check_index - self.current_check_index) % 8 == 0 or
                    (check_index // 8 == self.current_check_index // 8)):
                indexes_of_possible_moves.append(check_index)
        return indexes_of_possible_moves


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


class Pawn(Figure):

    def __init__(self, check_index, colour, chessboard):
        super().__init__(check_index, "pawn.png", colour, "Pawn", chessboard)
        self.__firstMove = True

    def check_for_all_possible_moves(self):
        indexes_of_possible_moves = []
        if self.colour == "black":
            side_of_moving_coef = 1
        else:
            side_of_moving_coef = -1

        possible_move = self.current_check_index + 8 * side_of_moving_coef
        if self.firstMove:
            indexes_of_possible_moves.append(possible_move)
            indexes_of_possible_moves.append(possible_move + 8 * side_of_moving_coef)
            indexes_of_possible_moves.append(self.current_check_index)

        else:
            indexes_of_possible_moves.append(possible_move)
            indexes_of_possible_moves.append(self.current_check_index)

        new_indexes_of_possible_moves = indexes_of_possible_moves
        for index in indexes_of_possible_moves:
            if self.chessboard.get_check(index).hasFigure:
                new_indexes_of_possible_moves.remove(index)

        eat_moves = [self.current_check_index + 7, self.current_check_index - 7,
                     self.current_check_index + 9, self.current_check_index - 9]

        correct_eat_moves = []

        for move_index in range(0, len(eat_moves)):
            if side_of_moving_coef == -1 and eat_moves[move_index] < self.current_check_index \
                    and self.chessboard.get_check(eat_moves[move_index]).hasFigure:
                correct_eat_moves.append(eat_moves[move_index])
            if side_of_moving_coef == 1 and eat_moves[move_index] > self.current_check_index\
                    and self.chessboard.get_check(eat_moves[move_index]).hasFigure:
                correct_eat_moves.append(eat_moves[move_index])

        new_indexes_of_possible_moves.append(self.current_check_index)
        new_indexes_of_possible_moves += correct_eat_moves

        return new_indexes_of_possible_moves



    @motion_decorator
    def move_to(self, next_check_index):
        """Перемещает фигуру"""
        if next_check_index in self.check_for_all_possible_moves() and self.current_check_index != next_check_index:

            if self.chessboard.get_check(next_check_index).hasFigure:
                self.chessboard.get_check(next_check_index).figure.die()

                self.last_move = "{0} {1} has eaten {2} {3}" \
                                 " and was moved from {4} check to {5}" \
                    .format(self.colour, self.name,
                            self.chessboard.get_check(next_check_index).figure.colour,
                            self.chessboard.get_check(next_check_index).figure.name,
                            self.current_check_index, next_check_index)

                self.current_check_index = next_check_index
            else:

                self.last_move = "{0} {1} was moved from {2} check to {3}" \
                    .format(self.colour, self.name,
                            self.current_check_index, next_check_index)

                self.current_check_index = next_check_index

            if self.colour == "white" and self.current_check_index // 8 == 0:
                self.kill()
                raise FigureException("white")
            elif self.colour == "black" and self.current_check_index // 8 == 7:
                raise FigureException("black")
                self.kill()

            if self.firstMove:
                self.firstMove = False

    def turn_into_queen(self):
        if self.colour == "white" and self.current_check_index // 8 == 0:
            return Queen(self.current_check_index, "white", self.chessboard)
            # self.kill()
        elif self.colour == "black" and self.current_check_index // 8 == 7:
            return Queen(self.current_check_index, "black", self.chessboard)
            # self.kill()
        else:
            return None

    @property
    def firstMove(self):
        """Имеет фигуру или нет"""
        return self.__firstMove

    @firstMove.setter
    def firstMove(self, firstMove):
        """Сеттер hasFigure"""
        self.__firstMove = firstMove

class Horse(Figure):
    def __init__(self, check_index, colour, chessboard):
        super().__init__(check_index, "horse.png", colour, "Horse", chessboard)

    def check_for_all_possible_moves(self):

        if self.colour == "black":
            killable_colour = "white"

        else:
            killable_colour = "black"

        indexes_of_possible_moves = []

        if ((self.current_check_index // 8) - (self.current_check_index + 10) // 8) == -1:
            indexes_of_possible_moves.append(self.current_check_index + 10)

        if ((self.current_check_index // 8) - (self.current_check_index - 10) // 8) == 1:
            indexes_of_possible_moves.append(self.current_check_index - 10)

        if ((self.current_check_index // 8) - (self.current_check_index + 15) // 8) == -2:
            indexes_of_possible_moves.append(self.current_check_index + 15)

        if ((self.current_check_index // 8) - (self.current_check_index - 15) // 8) == 2:
            indexes_of_possible_moves.append(self.current_check_index - 15)

        if ((self.current_check_index // 8) - (self.current_check_index - 6) // 8) == 1:
            indexes_of_possible_moves.append(self.current_check_index - 6)

        if ((self.current_check_index // 8) - (self.current_check_index + 17) // 8) == -2:
            indexes_of_possible_moves.append(self.current_check_index + 17)

        if ((self.current_check_index // 8) - (self.current_check_index - 17) // 8) == 2:
            indexes_of_possible_moves.append(self.current_check_index - 17)

        if ((self.current_check_index // 8) - (self.current_check_index + 6) // 8) == -1:
            indexes_of_possible_moves.append(self.current_check_index + 6)

        new_indexes_of_possible_moves = []
        for index in indexes_of_possible_moves:
            if 0 <= index < 64 and not self.chessboard.get_check(index).hasFigure:
                new_indexes_of_possible_moves.append(index)

            elif 0 <= index < 64 and self.chessboard.get_check(index).figure.colour == killable_colour:
                new_indexes_of_possible_moves.append(index)

        new_indexes_of_possible_moves.append(self.current_check_index)
        return new_indexes_of_possible_moves