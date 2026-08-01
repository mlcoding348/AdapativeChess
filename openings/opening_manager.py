import chess

from openings.queen_gambit import QUEENS_GAMBIT


class OpeningManager:

    def __init__(self):

        self.moves = []

        self.current_move = 0

        self.name = None


    def load_opening(
        self,
        opening_name,
        variation_name
    ):

        if opening_name == "Queen's Gambit":

            self.moves = QUEENS_GAMBIT[variation_name]

        else:

            raise ValueError(
                "Opening not supported"
            )


        self.current_move = 0

        self.name = variation_name



    def reset(self):

        self.current_move = 0



    def has_next_move(self):

        return self.current_move < len(self.moves)



    def get_next_move(self):

        if self.has_next_move():

            return self.moves[self.current_move]

        return None



    def player_move_correct(
        self,
        move
    ):

        expected = self.get_next_move()


        if move == expected:

            self.current_move += 1

            return True


        return False



    def get_expected_move(self):

        return self.get_next_move()