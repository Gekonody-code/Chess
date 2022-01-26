import pygame
from Chess_board import Chessboard
import os
import os.path
from abc import ABC, abstractmethod
from functools import wraps
import time
from Additional_stuff import FigureException, motion_decorator


class Figure(ABC, pygame.sprite.Sprite):
    """Базовый класс, имитирующий некоторую фигуру"""

    def __init__(self, check_index, figureImg, colour, name, chessboard, isAlive=True):
        """Конструктор"""
        pygame.sprite.Sprite.__init__(self)
        if check_index > 63 or check_index < 0:
            raise FigureException("Вы пытаетесь поставить фигуру за пределами шахматной доски")
        #
        if colour != "white" and colour != "black":
            raise FigureException("Неверный цвет {0}. Цвет может быть либо black, либо white".format(colour))
        self.__current_check_index = check_index
        self.__figureImg = figureImg
        self.__colour = colour
        self.__name = name
        self.__isAlive = isAlive
        self.chessboard = chessboard
        # При создании фигуры меняет параметр клетки hasFigure на True
        check = self.chessboard.get_check(self.__current_check_index)
        check.hasFigure = True
        check.figure = self  # Передает себя в клетку в соответствующее поле

    def set_color(self):
        """Выбирает цвет и указывает директорию с картинкой"""
        self.__figureImg = self.__colour + "_" + self.__figureImg
        filename = "../Chess_project/Assets"
        file_path = os.path.abspath(filename)
        self.__figureImg = file_path + "\\" + self.__figureImg

    def draw_figure(self, screen, check):
        """Отрисовывает фигуру"""
        # Если фигура только создана, определяет ее цвет
        if "Assets" not in self.__figureImg:
            self.set_color()

        if self.isAlive:
            # print(self.name, self.isAlive)
            pict = pygame.image.load(self.__figureImg)
            screen.blit(pict, (check.checkX, check.checkY))  # Отрисовывает фигуру по указанным координатам

    def die(self):
        """Убивает фигуру"""
        self.isAlive = False
        self.chessboard.get_check(self.current_check_index).hasFigure= None

    @motion_decorator
    def move_to(self, next_check_index):
        """Перемещает фигуру"""
        # Проверяет можно ли походить в выбранную клетку и что выбранная клетка не совпадает с текущей
        if next_check_index in self.check_for_all_possible_moves() and self.__current_check_index != next_check_index:
            self.write_down_move_and_die(next_check_index)
            if self.chessboard.get_check(next_check_index).hasFigure:
                self.chessboard.get_check(next_check_index).figure.die()
            self.current_check_index = next_check_index


    def write_down_move_and_die(self, next_check_index):
        if self.chessboard.get_check(next_check_index).hasFigure:
            self.last_move = "{0} {1} has eaten {2} {3}" \
                             " and was moved from {4} check to {5}" \
                .format(self.colour, self.name,
                        self.chessboard.get_check(next_check_index).figure.colour,
                        self.chessboard.get_check(next_check_index).figure.name,
                        self.current_check_index, next_check_index)

        else:
            self.last_move = "{0} {1} was moved from {2} check to {3}" \
                .format(self.colour, self.name,
                        self.current_check_index, next_check_index)

    @abstractmethod
    def check_for_all_possible_moves(self):
        pass

    @property
    def current_check_index(self):
        """Индекс клетки, на которой стоит фигура"""
        return self.__current_check_index

    @property
    def name(self):
        """Имя фигуры"""
        return self.__name

    @property
    def colour(self):
        """Цвет фигуры"""
        return self.__colour

    @property
    def figureImg(self):
        """Спрайт фигуры"""
        return self.__figureImg

    @property
    def isAlive(self):
        """Жива фигура или нет"""
        return self.__isAlive

    @property
    def selected(self):
        """Выбрана фигура или нет"""
        return self.__selected

    @current_check_index.setter
    def current_check_index(self, new_check_index):
        """Сеттер индекса клетки"""
        # Нужен для перемещения фигуры Как только фигура перемещается, меняет у прошлой клеточки hasFigure на False и,
        # указывает что на ней теперь не стоит фигуры.
        # А на новой наоборот задает, что фигура там теперь стоит

        if new_check_index > 63 or new_check_index < 0:
            raise FigureException("Вы пытаетесь поставить фигуру за пределами шахматной доски")
        else:
            past_check = self.chessboard.get_check(self.__current_check_index)
            past_check.hasFigure = False
            past_check.figure = None
            new_check = self.chessboard.get_check(new_check_index)
            new_check.hasFigure = True
            new_check.figure = self
            self.__current_check_index = new_check_index

    @selected.setter
    def selected(self, selected):
        """Сеттер selected"""
        self.__selected = selected

    @isAlive.setter
    def isAlive(self,isAlive):
        self.__isAlive = isAlive

    def __eq__(self, other):
        """Переопределение базового оператора равенства"""
        return self.__name == other.name and self.__colour == other.colour

    def __ne__(self, other):
        """Переопределение базового оператора неравенства"""
        return self.__name != other.name and self.__colour != other.colour


