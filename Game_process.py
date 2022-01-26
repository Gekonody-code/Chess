import datetime
from Sqlite_db_chess import save_game_in_db


class GameProcess():
    def __init__(self, which_turn, figures, start_time):
        self.running = True
        self.which_turn = which_turn
        self.start_time = start_time
        self.black_figures = []
        self.white_figures = []
        for figure in figures:
            if figure.name == "King":
                if figure.colour == "black":
                    self.black_king = figure
                else:
                    self.white_king = figure
            else:
                if figure.colour == "black":
                    self.black_figures.append(figure)
                else:
                    self.white_figures.append(figure)

    def turn(self):
        all_enemy_moves = []
        if self.which_turn == "white":
            for figure in self.white_figures:
                all_enemy_moves += figure.check_for_all_possible_moves()
            if set(self.black_king.check_for_all_possible_moves()).issubset(all_enemy_moves):
                self.win("white")
            self.which_turn = "black"

        elif self.which_turn == "black":
            for figure in self.black_figures:
                all_enemy_moves += figure.check_for_all_possible_moves()
            if set(self.white_king.check_for_all_possible_moves()).issubset(all_enemy_moves):
                self.win("black")
            self.which_turn = "white"

    def win(self, colour_of_winners):

        game_duration = datetime.timedelta(seconds=self.start_time)
        print(f"{colour_of_winners} победили за {str(game_duration)}")

        f = open("history_of_the_game.txt", 'r')
        history_of_game = f.read()
        save_game_in_db(colour_of_winners, str(game_duration), history_of_game, )
        self.running = False