from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
)

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

        # Chess board
        self.board = ChessBoard()

        # Stockfish engine
        self.engine = ChessEngine()

        # Store complete turns:
        # [("e4", "e5"), ("Nf3", "Nc6"), ...]
        self.moves = []

        self.checks_given = 0

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

    def engine_move(self):
        """
        Human has already moved.
        Calculate SAN for both moves and let Stockfish respond.
        """

        #
        # Human move
        #

        human_move = self.board.board.peek()

        self.board.board.pop()
        human_san = self.board.board.san(human_move)
        self.board.board.push(human_move)

        #
        # Game over?
        #

        if self.board.board.is_game_over():

            self.moves.append(
                (human_san, "")
            )

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
        # Save complete turn
        #

        self.moves.append(
            (
                human_san,
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

        self.turn_label.setText(
            "Turn: White"
        )

    def closeEvent(self, event):
        """
        Properly close Stockfish.
        """

        self.engine.close()

        event.accept()