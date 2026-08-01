import chess
import chess.engine
import os


class ChessEngine:

    def __init__(self):

        engine_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "engine",
            "stockfish.exe"
        )

        self.engine = chess.engine.SimpleEngine.popen_uci(
            engine_path
        )

        self.elo = 3000

        self.update_strength()


    def update_strength(self):

        """
        Convert Elo rating into Stockfish Skill Level.
        """

        skill = int(
            max(
                0,
                min(
                    20,
                    (self.elo - 1000) / 100
                )
            )
        )

        self.engine.configure(
            {
                "Skill Level": skill
            }
        )


    def get_move(self, board):

        result = self.engine.play(
            board,
            chess.engine.Limit(
                depth=15
            )
        )

        return result.move


    def set_elo(self, elo):

        self.elo = max(
            1000,
            elo
        )

        self.update_strength()


    def decrease_elo(self, amount=100):

        self.set_elo(
            self.elo - amount
        )


    def get_elo(self):

        return self.elo


    def close(self):

        self.engine.quit()