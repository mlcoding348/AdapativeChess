from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
)

import chess
from openings.opening_manager import OpeningManager

from ui.chess_board import ChessBoard
from ui.engine import ChessEngine


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adaptive Chess")
        self.resize(1200, 800)

        layout = QHBoxLayout(self)

        info_panel = QVBoxLayout()

        self.elo_label = QLabel("Engine Elo: 3000")
        self.check_label = QLabel("Checks Given: 0")
        self.eval_label = QLabel("Evaluation: 0.00")
        self.turn_label = QLabel("Turn: White")

        self.history_label = QLabel(
            "Move History:\n"
        )

        info_panel.addWidget(self.elo_label)
        info_panel.addWidget(self.check_label)
        info_panel.addWidget(self.eval_label)
        info_panel.addWidget(self.turn_label)
        info_panel.addWidget(self.history_label)

        info_panel.addStretch()


        #
        # Chess board
        #

        self.board = ChessBoard()


        #
        # Stockfish engine
        #

        self.engine = ChessEngine()


        #
        # Temporary opening test:
        #
        # Queen's Gambit
        #
        # 1. d4 d5
        # 2. c4
        #
        # Black to move
        #

        self.opening_manager = OpeningManager()
        fen = self.opening_manager.load_opening(
            "Queen's Gambit",
            "Queen's Gambit Declined"
        )

        self.board.load_position(fen)


        #
        # Store moves
        #

        self.moves = []

        self.checks_given = 0


        #
        # Signals
        #

        self.board.move_made.connect(
            self.engine_move
        )

        self.board.check_given.connect(
            self.player_check
        )


        layout.addLayout(info_panel, 1)
        layout.addWidget(self.board, 3)


        self.setStyleSheet("""
            QWidget {
                background-color: #202124;
                color: white;
                font-size: 16px;
            }

            QLabel {
                padding: 5px;
            }
        """)


        #
        # If opening starts with Black,
        # Stockfish plays first
        #

        if self.board.board.turn == chess.BLACK:

            self.engine_move()


    def engine_move(self):
        """
        Stockfish makes a move.

        Supports:
        - Normal game after human move
        - Opening practice where engine starts
        """


        #
        # Game over?
        #

        if self.board.board.is_game_over():

            self.update_history()

            return


        #
        # Engine move
        #

        engine_move = self.engine.get_move(
            self.board.board
        )


        engine_san = self.board.board.san(
            engine_move
        )


        self.board.make_engine_move(
            engine_move
        )


        #
        # Save engine move
        #

        self.moves.append(
            (
                "",
                engine_san
            )
        )


        self.update_history()



    def player_check(self):
        """
        Human gave check.
        Lower Stockfish strength.
        """

        self.checks_given += 1

        self.engine.decrease_elo(100)

        self.check_label.setText(
            f"Checks Given: {self.checks_given}"
        )

        self.elo_label.setText(
            f"Engine Elo: {self.engine.get_elo()}"
        )


    def update_history(self):

        history = "Move History:\n\n"

        for move_number, (white, black) in enumerate(
            self.moves,
            start=1
        ):

            history += (
                f"{move_number}. {white} {black}\n"
            )


        self.history_label.setText(
            history
        )


        if self.board.board.turn == chess.WHITE:

            self.turn_label.setText(
                "Turn: White"
            )

        else:

            self.turn_label.setText(
                "Turn: Black"
            )


    def closeEvent(self, event):
        """
        Properly close Stockfish.
        """

        self.engine.close()

        event.accept()