import pygame
from Additional_stuff import Mixin_Higlighter

class Check (pygame.Rect, Mixin_Higlighter):

    def __init__(self, checkX, checkY, color, size):
        """Конструктор клетки"""
        self.__color = color
        self.__checkX = checkX
        self.__checkY = checkY
        self.__size = size
        self.__figure = None
        self.__hasFigure = False

    def draw_check(self, screen, color = None):
        """Отрисовывает клетку на экране"""
        if color is None:  # Если нет параметра color, то рисуется дефолтный цвет клетки. Нужно для выделения клетки
            color = self.__color
        pygame.draw.rect(screen, color, (self.__checkX, self.__checkY, self.__size, self.__size))

    def draw_check_tkinter(self,canvas):
        canvas.create_rectangle(self.__checkX, self.__checkY,
                                self.__checkX + self.__size, self.__checkY + self.__size,
                                fill=self.__color)

    @property
    def hasFigure(self):
        """Имеет фигуру или нет"""
        return self.__hasFigure

    @hasFigure.setter
    def hasFigure(self, hasFigure):
        """Сеттер hasFigure"""
        self.__hasFigure = hasFigure

    @property
    def checkX(self):
        """Координата клетки по X"""
        return self.__checkX

    @checkX.setter
    def checkX(self, checkX):
        """Сеттер checkX"""
        self.__checkX = checkX

    @property
    def checkY(self):
        """Координата клетки по Y"""
        return self.__checkY

    @checkY.setter
    def checkY(self, checkY):
        """Сеттер checkY"""
        self.__checkY = checkY

    @property
    def color(self):
        """Цвет клетки"""
        return self.__color

    @color.setter
    def color(self, color):
        """Сеттер color"""
        self.__color = color

    @property
    def figure(self):
        """Фигура, стоящая на этой клетке"""
        return self.__figure

    @figure.setter
    def figure(self, figure):
        """Сеттер figure"""
        self.__figure = figure

