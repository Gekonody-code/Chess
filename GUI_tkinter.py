import tkinter as tk
import asyncio
from Chess_board import Chessboard

class GUI_chess_menu(tk.Tk):
    """Интерфейс меню"""
    def __init__(self, width_of_the_window, height_of_the_window, game_func):
        super().__init__()

        self.width_of_the_window = width_of_the_window
        self.height_of_the_widow = height_of_the_window
        self.game_func = game_func
        w = self.winfo_screenwidth()  # Получаем ширину и высоту экрана
        h = self.winfo_screenheight()
        w = w // 2 - (self.width_of_the_window // 2)  # Находим середину, для того, чтобы поместить окно туда
        h = h // 2 - (self.height_of_the_widow // 2)
        self.resizable(False, False) # Запрещаем изменять размер окна
        # Устанавливаем размер окна и где оно появляется
        self.geometry("{}x{}+{}+{}".format(self.width_of_the_window, self.height_of_the_widow, w, h))

        # Создаем холст и отрисовываем на нем доску
        self.canvas = tk.Canvas(self, width=width_of_the_window, height=height_of_the_window, bg='gray')
        chessboard = Chessboard(width_of_the_window)
        chessboard.init_checks_tkinter()
        chessboard.draw_chess_board_tkinter(self.canvas)
        self.canvas.create_rectangle(68,115,444,398,fill="white")
        self.canvas.create_text(200,151,anchor=tk.NW, text="Chess:", font=("Ubuntu",33))
        self.canvas.create_text(138, 195, anchor=tk.NW, text="Battle Royale", font=("Ubuntu",33))
        self.canvas.create_text(203, 249, anchor=tk.NW, text="by Renat", font=("Ubuntu",22), fill="#755334")
        self.canvas.pack()

        # Создаем кнопки войти и выйти
        self.quit_button = menuButton(text="Quit")
        self.play_button = menuButton(text="Start game")
        self.play_button.bind('<Button-1>', self.play_game) # Привязываем кнопки к функциям
        self.quit_button.bind('<Button-1>', self.quit_game)
        self.quit_button.place(x=272, y=322, height=48, width=141, bordermode=tk.OUTSIDE)
        self.play_button.place(x=108, y=322, height=48, width=141, bordermode=tk.OUTSIDE)


    def play_game(self, event):
        """Закрывает окно и запускает игру"""
        self.destroy()
        asyncio.run(self.game_func)
        # self.game_func()

    def quit_game(self, event):
        """Просто закрывает окно"""
        self.destroy()



class menuButton(tk.Button):
    """Класс кнопки меню"""
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)

        self['background'] = "black",
        self['activebackground'] = "#42190e",
        self['foreground'] = "white",
        self['activeforeground'] = '#f5f5f5',
        self['padx'] = "20",
        self['pady'] = "8",
        self['font'] = ("Verdana", 13, "bold"),
        self['relief'] = tk.RAISED,






