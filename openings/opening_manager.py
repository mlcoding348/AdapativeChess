import chess

class OpeningManager:

    def __init__(self):
        self.board = chess.Board()
        self.moves = []


    def load_opening(self, moves):

        self.board.reset()

        for move in moves:
            self.board.push_san(move)

        return self.board


    def get_position(self):

        return self.board.fen()