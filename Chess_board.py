import pygame

from Сheck import Check


class Chessboard:

    def __init__(self, sizeOfBoard=None):
        self.__checks = []
        if sizeOfBoard is None:
            pass
        else:
            self.__sizeOfBoard = sizeOfBoard
            self.unit = sizeOfBoard / 8

    def init_checks(self):
        """Инициализирует все клетки шахматного поля"""
        checkY = 0
        for row_index in range(8):
            self.init_row(checkY)
            checkY += self.unit

    def init_row(self, firstCheckY):
        """Инициализирует ряд клеток и добавляет его в checks[]"""
        checkX = 0
        checkY = firstCheckY

        # Выбор первого цвета в ряду в зависимости от номера ряда
        if (firstCheckY / self.unit) % 2 == 0:
            first_color = (255, 228, 205)
            second_color = (128, 73, 26)
        else:
            first_color = (128, 73, 26)
            second_color = (255, 228, 205)

        for i in range(8):
            if i % 2 == 0:
                current_check = Check(checkX, checkY, first_color, self.unit)
                checkX += self.unit
            else:
                current_check = Check(checkX, checkY, second_color, self.unit)
                checkX += self.unit

            self.__checks.append(current_check)

    def find_check_by_coordinates(self, x, y):
        """Возвращает клетку по данным координатам"""
        x //= self.unit
        y //= self.unit
        for check in self.__checks:
            if (check.checkX / self.unit == x) & (check.checkY / self.unit == y):
                return check

    def draw_chess_board(self, screen):
        """Отрисовывает клетки на экране"""
        # if not self.__checks:
        #     self.init_checks()
        for check in self.__checks:
            check.draw_check(screen)


    @property
    def get_checks(self):
        """Возвращает список клеток"""
        return self.__checks

    def get_check(self, check_index):
        """Возвращает клетку по данному индексу"""
        return self.__checks[check_index]

    def get_check_index_with_coordinates(self, x, y):
        """Возвращает индекс клетки по данным координатам"""
        for i in range(len(self.__checks)):
            if (self.__checks[i].checkX // self.unit == x // self.unit) & (
                    self.__checks[i].checkY // self.unit == y // self.unit):
                return i


    def init_checks_tkinter(self):
        """Инициализирует все клетки шахматного поля"""
        checkY = 0
        for row_index in range(8):
            self.init_row_tkinter(checkY)
            checkY += self.unit

    def draw_chess_board_tkinter(self,canvas):
        for check in self.__checks:
            check.draw_check_tkinter(canvas)

    def init_row_tkinter(self, firstCheckY):
        """Инициализирует ряд клеток и добавляет его в checks[]"""
        checkX = 0
        checkY = firstCheckY

        # Выбор первого цвета в ряду в зависимости от номера ряда
        if (firstCheckY / self.unit) % 2 == 0:
            first_color = "#93897d"
            second_color = "#4b2c10"
        else:
            first_color = "#4b2c10"
            second_color = "#93897d"

        for i in range(8):
            if i % 2 == 0:
                current_check = Check(checkX, checkY, first_color, self.unit)
                checkX += self.unit
            else:
                current_check = Check(checkX, checkY, second_color, self.unit)
                checkX += self.unit

            self.__checks.append(current_check)