from Figures import Figure
import time
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
