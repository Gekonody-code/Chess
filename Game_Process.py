import datetime
import threading
import pygame
import os
import os.path
import random
from Additional_stuff import *
from Chess_board import Chessboard
from Chess_figures import *
import asyncio
from GUI_tkinter import *
from Sqlite_db_chess import save_game_in_db

selected = None

#Определяет чей ход
which_turn = 'white'

WIDTH = 512
HEIGHT = 512
FPS = 30
async def start_Game():
    # Задаем цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Создаем игру и окно
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()


    # filename = "Assets"
    # file_path = os.path.abspath(filename)
    # icon = pygame.image.load(file_path + "\\" + "white_rook.png")

    def init_rooks(chessboard):
        """Инициализирует ладей"""
        rooks = []
        rooks.append(Rook(0, "black", chessboard))
        rooks.append(Rook(7, "black", chessboard))
        rooks.append(Rook(56, "white", chessboard))
        rooks.append(Rook(63, "white", chessboard))
        return rooks


    def init_bishops(chessboard):
        """Инициализирует слонов"""
        bishops = []
        bishops.append(Bishop(2, "black", chessboard))
        bishops.append(Bishop(5, "black", chessboard))
        bishops.append(Bishop(58, "white", chessboard))
        bishops.append(Bishop(61, "white", chessboard))
        return bishops


    def init_queens(chessboard):
        """Инициирует ферзей"""
        queens = []
        queens.append(Queen(3, "black", chessboard))
        queens.append(Queen(59, "white", chessboard))
        return queens


    def init_pawns(chessboard):
        """Инициализирует пешки"""
        pawns = []
        for black_pawn_index in range(8, 16):
            white_pawn_index = black_pawn_index + 40
            pawns.append(Pawn(black_pawn_index, "black", chessboard))
            pawns.append(Pawn(white_pawn_index, "white", chessboard))
        return pawns

    def init_horses(chessboard):
        horses = []
        horses.append(Horse(1, "black", chessboard))
        horses.append(Horse(6, "black", chessboard))
        horses.append(Horse(57, "white", chessboard))
        horses.append(Horse(62, "white", chessboard))
        return horses

    def init_kings(chessboard):
        kings = []
        kings.append(King(4, "black", chessboard))
        kings.append(King(60, "white", chessboard))
        return kings

    def draw_figures_from_list(figures):
        """Отрисовывает фигуры из листа"""
        for figure in figures:
            figure_index = figure.current_check_index
            figure.draw_figure(screen, chessboard.get_check(figure_index))


    # Инициализация объектов
    chessboard = Chessboard(WIDTH)
    # Создание потока, инициализирующего доску
    chessboard_thread = FiguresInitThread(target=chessboard.init_checks(), name="chessboard")
    chessboard_thread.start()
    chessboard_thread.join()

    # Создание потоков для инициализации фигур
    rooks_thread = FiguresInitThread(target=init_rooks, args=(chessboard,), name="rooks")
    bishops_thread = FiguresInitThread(target=init_bishops, args=(chessboard,), name="bishops")
    queens_thread = FiguresInitThread(target=init_queens, args=(chessboard,), name="queens")
    pawns_thread = FiguresInitThread(target=init_pawns, args=(chessboard,), name="pawns")
    horses_thread = FiguresInitThread(target=init_horses, args=(chessboard,), name="horses")
    kings_thread = FiguresInitThread(target=init_kings, args=(chessboard,), name="kings")
    rooks_thread.start()
    bishops_thread.start()
    queens_thread.start()
    pawns_thread.start()
    horses_thread.start()
    kings_thread.start()

    rooks = rooks_thread.join()
    bishops = bishops_thread.join()
    queens = queens_thread.join()
    pawns = pawns_thread.join()
    horses = horses_thread.join()
    kings = kings_thread.join()

    # figures = []
    # # figures += rooks + bishops + queens + pawns + horses + kings
    # rooks = init_rooks(chessboard)
    # bishops = init_bishops(chessboard)
    # queens = init_queens(chessboard)
    # pawns = init_pawns(chessboard)

    # Создание исключений
    # pawns.append(Pawn(65, "black", chessboard))
    # queens.append(Queen(30, "yellow", chessboard))

    # Цикл игры
    global which_turn
    f = open('history_of_the_game.txt', 'w')
    f.close()

    # hurry_task = asyncio.create_task(hurry_the_player(5))
    # hurry_task


    running = True
    start_time = pygame.time.get_ticks()
    previous_figure = chessboard.get_check(0).figure

    while running:

        # Держим цикл на правильной скорости
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        delta_time_s = (current_time - start_time) // 1000

        # Обновление

        # hurry_task = asyncio.create_task(hurry_the_player(5))
        # await hurry_task
        # Рендеринг
        chessboard.draw_chess_board(screen)

        # Ввод процесса (события)

        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Если нажали на кнопку мыши
                pos = pygame.mouse.get_pos()  # Координаты курсора в кортеже x,y
                start_check_color = None
                index_colors_dict = {}

                x = pos[0]
                y = pos[1]

                # Находим ячейку по координатам, проверяем, если там есть фигура
                # Если есть подсвечиваем все возможные ходы
                selected_check = chessboard.find_check_by_coordinates(x, y)
                if selected_check.hasFigure: #and selected_check.figure.colour == which_turn:
                    possible_moves = selected_check.figure.check_for_all_possible_moves()
                    for index in possible_moves:
                        # Словарь нужен, чтобы вернуть цвета к исходным
                        index_colors_dict[index] = chessboard.get_check(index).color
                    selected_check.highlight_possible_moves((255, 215, 0), chessboard, possible_moves)

            if event.type == pygame.MOUSEBUTTONUP:
                # Если кнопку мыши отпустили
                # Проверка на то что в выбранной клетке есть фигура и она соответствует цвету который сейчас ходит
                if selected_check.hasFigure: #and selected_check.figure.colour == which_turn:
                    (x, y) = pygame.mouse.get_pos()
                    new_check_index = chessboard.get_check_index_with_coordinates(x, y)
                    # Получили индекс клетки где мышку отпустили
                    try:
                        # Фигуру, стоявшую на месте, где была нажата кнопка, двигаем в клетку, где кнопку отпустили
                        current_figure = selected_check.figure
                        # Для корректного логгирования, запрещаем ходить на месте и в невозможные клетки
                        if selected_check.figure.current_check_index != new_check_index \
                                and new_check_index in current_figure.check_for_all_possible_moves():
                            current_figure.move_to(new_check_index)
                            log_task = asyncio.create_task(log_history_of_game(current_figure.last_move))
                            await log_task

                            if previous_figure.name == "Pawn" and previous_figure.justDidFirstMove:
                                previous_figure.justDidFirstMove = False

                            previous_figure = current_figure
                            # После совершения хода, меняем, чей ход сейчас
                            if which_turn == "white":
                                which_turn = "black"
                            else:
                                which_turn = "white"



                    except FigureException as pawnTrigger:
                        # Данное исключение триггер, который сработает, только если фигура пешка и она дошла до конца поля
                        for i in range(len(pawns)):
                            if pawns[i] is current_figure:
                                ex_pawn_index = i
                        pawns.pop(ex_pawn_index)
                        new_queen = Queen(current_figure.current_check_index, pawnTrigger.message,
                                          current_figure.chessboard)
                        queens.append(new_queen)

                        if which_turn == "white":
                            which_turn = "black"
                        else:
                            which_turn = "white"

                    selected_check.cancel_highlight(index_colors_dict, chessboard)


        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            running = win(which_turn, delta_time_s)

        draw_figures_from_list(rooks)
        draw_figures_from_list(bishops)
        draw_figures_from_list(queens)
        draw_figures_from_list(pawns)
        draw_figures_from_list(horses)
        draw_figures_from_list(kings)
        # draw_figures_from_list(figures)

        # После отрисовки всего, переворачиваем экран
        pygame.display.update()

    pygame.quit()


async def log_history_of_game(info_about_move):
    """Записывает информацию о ходе в файл"""
    if info_about_move is not None:
        if os.path.exists('history_of_the_game.txt'):
            with open("history_of_the_game.txt", "a") as f:  # открываем файл на запись, если он существует
                f.write(info_about_move + "\n")  # записываем элементы в файл
        else:
            with open("history_of_the_game.txt", "x") as f:  # создаем файл на запись, если его не существует
                f.write(info_about_move + "\n")

async def main():
    """Создание таска игры"""
    game_task = asyncio.create_task(start_Game())
    await game_task


def win(colour_of_winners, duration_of_the_game):

    game_duration = datetime.timedelta(seconds=duration_of_the_game)
    break_loop_signal = False
    print(f"{colour_of_winners} победили за {str(game_duration)}")

    f = open("history_of_the_game.txt", 'r')
    history_of_game = f.read()
    save_game_in_db(colour_of_winners, str(game_duration), history_of_game, )
    return break_loop_signal


# Создание GUI меню с помощью библиотеки tkinter

menu = GUI_chess_menu(WIDTH, HEIGHT, main())
menu.title("Chess")  # Устанавливаем название окну
menu.mainloop()
