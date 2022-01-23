import threading
import time

"""ДЕКОРАТОР ВОЗМОЖНЫХ ХОДОВ"""
def possible_move_decorator(func):
    """Декорирует функции, проверяющие возможности хода, запрещая им ходить через фигуры"""

    def wrapper(self):
        # Предусловие, определяющее фигуры, какого цвета можно убить
        if self.colour == "white":
            killable_colour = "black"
        elif self.colour == "black":
            killable_colour = "white"

        indexes_of_possible_moves = func(self)
        new_indexes_of_possible_moves = list(indexes_of_possible_moves)
        deleted_indexes = []

        # Удаляет все клетки возможных ходов, где стоят фигуры
        for possible_index in indexes_of_possible_moves:
            if self.chessboard.get_check(possible_index).hasFigure:
                if self.current_check_index != possible_index:
                    deleted_indexes.append(possible_index)
                    new_indexes_of_possible_moves.remove(possible_index)

        # Цикл, реализующий постусловие, которое удаляет из возможность ходить за фигуры
        for deleted_index in deleted_indexes:

            # Если фигура в одном ряду, с выбранной фигурой, то надо удалить все клетки за препятствующей фигурой
            if (8 > self.current_check_index - deleted_index > -8) \
                    and (self.current_check_index // 8 == deleted_index // 8):
                row = self.current_check_index // 8
                while deleted_index // 8 == row and deleted_index > 0:
                    if self.current_check_index > deleted_index:
                        if deleted_index in new_indexes_of_possible_moves:
                            # print("УДАЛЯЮ: ", deleted_index)
                            new_indexes_of_possible_moves.remove(deleted_index)
                        deleted_index -= 1
                    else:
                        if deleted_index in new_indexes_of_possible_moves:
                            new_indexes_of_possible_moves.remove(deleted_index)
                        deleted_index += 1

            # Если препятствующая фигура, ниже выбранной - удалить все возможные ходы за ней
            elif self.current_check_index < deleted_index:
                while True:
                    # Проверяет три клетки за занятой клеткой, если там есть возможный ход, удаляет его
                    # Затем удаленную клеточку делает выбранной, и проверяет три клетки за ней
                    # Как только за текущей клеткой нет возможной клетки, цикл заканчивается
                    vertical_check = deleted_index + 8
                    left_d_check = deleted_index + 7
                    right_d_check = deleted_index + 9
                    if vertical_check in new_indexes_of_possible_moves:
                        deleted_index = vertical_check
                        new_indexes_of_possible_moves.remove(vertical_check)
                    elif left_d_check in new_indexes_of_possible_moves:
                        deleted_index = left_d_check
                        new_indexes_of_possible_moves.remove(left_d_check)
                    elif right_d_check in new_indexes_of_possible_moves:
                        deleted_index = right_d_check
                        new_indexes_of_possible_moves.remove(right_d_check)
                    else:
                        break
            else:
                # Если препятствующая фигура, выше выбранной - удалить все возможные ходы за ней
                while True:
                    # Проверяет три клетки за занятой клеткой, если там есть возможный ход, удаляет его
                    # Затем удаленную клеточку делает выбранной, и проверяет три клетки за ней
                    # Как только за текущей клеткой нет возможной клетки, цикл заканчивается
                    vertical_check = deleted_index - 8
                    left_d_check = deleted_index - 7
                    right_d_check = deleted_index - 9
                    if vertical_check in new_indexes_of_possible_moves:
                        deleted_index = vertical_check
                        new_indexes_of_possible_moves.remove(vertical_check)
                    elif left_d_check in new_indexes_of_possible_moves:
                        deleted_index = left_d_check
                        new_indexes_of_possible_moves.remove(left_d_check)
                    elif right_d_check in new_indexes_of_possible_moves:
                        deleted_index = right_d_check
                        new_indexes_of_possible_moves.remove(right_d_check)
                    else:
                        break

        neighbours_of_deleted_indexes = []
        restored_indexes = []
        for deleted_index in deleted_indexes:
            # Восстановить в возможные клетки, где есть фигура вражеского цвета, чтобы ее можно было убить
            # Проверяет все соседние клетки, и добавляет их в список соседей удаленной клетки
            if self.chessboard.get_check(deleted_index).figure.colour == killable_colour:

                for i in range(3):
                    if deleted_index // 8 != 7:
                        if (deleted_index + 7 + i) // 8 == deleted_index // 8 + 1:
                            neighbours_of_deleted_indexes.append(deleted_index + 7 + i)
                    if deleted_index // 8 != 0:
                        if (deleted_index - 7 - i) // 8 == deleted_index // 8 - 1:
                            neighbours_of_deleted_indexes.append(deleted_index - 7 - i)
                if deleted_index % 8 != 0:
                    neighbours_of_deleted_indexes.append(deleted_index - 1)
                if deleted_index % 8 != 7:
                    neighbours_of_deleted_indexes.append(deleted_index + 1)

                # Если в соседях удаленной клетки, есть возможная клетка, то удаленная клетка добавляется в список восстановленных ходов
                # Таким образом мы восстанавливаем только те клетки с фигурами, которые будут первыми на пути выбранной фигуры
                for index in neighbours_of_deleted_indexes:
                    if index in new_indexes_of_possible_moves:
                        # print("vosstanavlivayu ", deleted_index)
                        restored_indexes.append(deleted_index)
                neighbours_of_deleted_indexes = []

        # Переносим все восстановленные клетки в список доступных ходов
        for index in restored_indexes:
            new_indexes_of_possible_moves.append(index)
        return new_indexes_of_possible_moves

    return wrapper

"""ДЕКОРАТОР ХОДОВ"""
def motion_decorator(func):
    """Регистрирует вызовы функций перемещения фигур"""
    # Копирование имени, документации и сигнатуры функции
    @wraps(func)
    def wrapper(self, next_check_index):
        start = time.time()
        # Обозначение начала выполнения хода
        starting_check = self.current_check_index
        print("Начало нового хода: {0} {1} ".format(self.colour, self.name))
        func(self, next_check_index)
        end = time.time()
        print("Фигура передвинута с {0} ячейки на {1}".format(starting_check, next_check_index))
        print("[*] Ход выполнен за {} секунд\n".format(end - start))
        # Обозначение конца
    return wrapper

"""КЛАСС ИСКЛЮЧЕНИЙ"""
class FigureException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print("calling str")
        if self.message:
            return 'FigureException, {0}'.format(self.message)
        else:
            return 'FigureException has been raised'

from functools import wraps

"""МЕТАКЛАСС"""
def debug(func):
    """Декоратор для указания вызываемой функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Переход к методу:", func.__qualname__)
        return func(*args, **kwargs)
    return wrapper


def debug_methods(cls):
    """Отладка методов класса"""
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debug(val))
    return cls


class DebugMeta(type):
    """metaclass передает созданный класс для получения требуемой
       функциональности при отладке (debug_methods)"""
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)
        obj = debug_methods(obj)
        return obj

"""КЛАСС МНОГОПОТОЧНОСТИ"""
class FiguresInitThread(threading.Thread):
    """Класс для реализации многопоточности при создании фигур"""
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        print("Initializing ", self.name)
        # print(type(self._target))
        # print(self._target)
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)
            # print("VOZVR", self._return)

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return


"""КЛАСС МИКСИН"""
class Mixin_Higlighter:
    """Выделяет возможные ходы для фигуры"""
    def highlight_possible_moves(self, color, chessboard, indexes_of_highlighted_checks):

        for index in indexes_of_highlighted_checks:
            highlighted_check = chessboard.get_check(index)
            if highlighted_check.color == (255, 228, 205):
                highlighted_check.color = color
            else:
                highlighted_check.color = tuple([i / 1.5 for i in color])

    def cancel_highlight(self, index_color_dict, chessboard):
        for index, color in index_color_dict.items():
            check = chessboard.get_check(index)
            check.color = color