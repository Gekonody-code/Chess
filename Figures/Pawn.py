from Figures.Figures import Figure
from Additional_stuff import *

class Pawn(Figure):

    def __init__(self, check_index, colour, chessboard):
        super().__init__(check_index, "pawn.png", colour, "Pawn", chessboard)
        self.__firstMove = True
        self.__justDidFirstMove = False

    def check_for_all_possible_moves(self):
        enemy_colour = None
        indexes_of_possible_moves = []
        if self.colour == "black":
            side_of_moving_coef = 1
            enemy_colour = "white"
        else:
            side_of_moving_coef = -1
            enemy_colour = "black"

        possible_move = self.current_check_index + 8 * side_of_moving_coef
        if self.firstMove and not self.chessboard.get_check(possible_move).hasFigure:
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
                    and self.chessboard.get_check(eat_moves[move_index]).hasFigure \
                    and (abs((eat_moves[move_index]) // 8 - (self.current_check_index // 8)) == 1):
                correct_eat_moves.append(eat_moves[move_index])

            if side_of_moving_coef == 1 and eat_moves[move_index] > self.current_check_index \
                    and self.chessboard.get_check(eat_moves[move_index]).hasFigure \
                    and (abs((eat_moves[move_index]) // 8 - (self.current_check_index // 8)) == 1):
                correct_eat_moves.append(eat_moves[move_index])

        right_figure = None
        left_figure = None
        if (self.current_check_index + 1) // 8 == self.current_check_index // 8:
            right_figure = self.chessboard.get_check(self.current_check_index + 1).figure
        if (self.current_check_index - 1) // 8 == self.current_check_index // 8:
            left_figure = self.chessboard.get_check(self.current_check_index - 1).figure

        if right_figure is not None:
            if right_figure.name == "Pawn":
                if right_figure.justDidFirstMove:
                    if side_of_moving_coef == 1:
                        correct_eat_moves.append(self.current_check_index + 9)
                    else:
                        correct_eat_moves.append(self.current_check_index - 7)

        if left_figure is not None:
            if left_figure.name == "Pawn":
                if left_figure.justDidFirstMove:
                    if side_of_moving_coef == 1:
                        correct_eat_moves.append(self.current_check_index + 7)
                    else:
                        correct_eat_moves.append(self.current_check_index - 9)

        new_indexes_of_possible_moves.append(self.current_check_index)
        new_indexes_of_possible_moves += correct_eat_moves

        remove_allies_indexes_list = []
        for index in new_indexes_of_possible_moves:
            if (self.chessboard.get_check(index).hasFigure
                and self.chessboard.get_check(index).figure.colour == enemy_colour) \
                    or not self.chessboard.get_check(index).hasFigure:
                remove_allies_indexes_list.append(index)

        new_indexes_of_possible_moves = remove_allies_indexes_list
        new_indexes_of_possible_moves.append(self.current_check_index)
        return new_indexes_of_possible_moves

    @motion_decorator
    def move_to(self, next_check_index):
        """Перемещает фигуру"""

        super(Pawn, self).move_to(next_check_index)
        if self.colour == "white" and self.current_check_index // 8 == 0:
            raise FigureException("white")
        elif self.colour == "black" and self.current_check_index // 8 == 7:
            raise FigureException("black")

        if self.firstMove:
            self.__justDidFirstMove = True
            self.firstMove = False

        if (self.colour == "white"
                and self.chessboard.get_check(next_check_index + 8).hasFigure
                and self.chessboard.get_check(next_check_index + 8).figure.name == "Pawn"
                and self.chessboard.get_check(next_check_index + 8).figure.justDidFirstMove):
            self.chessboard.get_check(next_check_index + 8).figure.die()

        elif (self.colour == "black"
              and self.chessboard.get_check(next_check_index - 8).hasFigure
              and self.chessboard.get_check(next_check_index - 8).figure.name == "Pawn"
              and self.chessboard.get_check(next_check_index - 8).figure.justDidFirstMove):
            self.chessboard.get_check(next_check_index - 8).figure.die()

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

    @property
    def justDidFirstMove(self):
        """Имеет фигуру или нет"""
        return self.__justDidFirstMove

    @justDidFirstMove.setter
    def justDidFirstMove(self, firstMove):
        """Сеттер hasFigure"""
        self.__justDidFirstMove = firstMove