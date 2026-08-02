from openings.queen_gambit import QUEENS_GAMBIT


class OpeningManager:


    def __init__(self):

        self.moves = []

        self.current_move = 0

        self.name = None

        self.opening = None



    def get_openings(self):

        return list(
            QUEENS_GAMBIT.keys()
        )



    def get_variations(
        self,
        opening_name
    ):

        if opening_name in QUEENS_GAMBIT:

            return list(
                QUEENS_GAMBIT[opening_name].keys()
            )

        return []



    def load_opening(
        self,
        opening_name,
        variation_name,
        color=None
    ):


        self.moves = QUEENS_GAMBIT[opening_name][variation_name]


        self.current_move = 0

        self.name = variation_name

        self.opening = opening_name



    def reset(self):

        self.current_move = 0



    def has_next_move(self):

        return self.current_move < len(self.moves)



    def get_next_move(self):

        if self.has_next_move():

            return self.moves[self.current_move]

        return None



    def advance_trainer_move(self):

        self.current_move += 1



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