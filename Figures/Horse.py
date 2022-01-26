from Figures.Figures import Figure


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
