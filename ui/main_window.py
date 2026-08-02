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
from ui.opening_panel import OpeningPanel


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "Adaptive Chess"
        )

        self.resize(
            1400,
            800
        )


        layout = QHBoxLayout(
            self
        )


        #
        # Info panel
        #

        info_panel = QVBoxLayout()


        self.elo_label = QLabel(
            "Engine Elo: 3000"
        )

        self.check_label = QLabel(
            "Checks Given: 0"
        )

        self.eval_label = QLabel(
            "Evaluation: 0.00"
        )

        self.turn_label = QLabel(
            "Turn: White"
        )

        self.history_label = QLabel(
            "Move History:\n"
        )

        self.history_label.setMaximumHeight(
            250
        )


        self.opening_label = QLabel(
            "Opening: None"
        )

        self.progress_label = QLabel(
            "Progress: 0 / 0"
        )

        self.status_label = QLabel(
            "Status: Ready"
        )


        info_panel.addWidget(self.elo_label)
        info_panel.addWidget(self.check_label)
        info_panel.addWidget(self.eval_label)
        info_panel.addWidget(self.turn_label)

        info_panel.addWidget(self.opening_label)
        info_panel.addWidget(self.progress_label)
        info_panel.addWidget(self.status_label)

        info_panel.addWidget(self.history_label)

        info_panel.addStretch()



        #
        # Board
        #

        self.board = ChessBoard()



        #
        # Engine
        #

        self.engine = ChessEngine()



        #
        # Opening manager
        #

        self.opening_manager = OpeningManager()



        #
        # Opening panel
        #

        self.opening_panel = OpeningPanel(
            self.opening_manager
        )


        self.opening_panel.training_started.connect(
            self.start_training
        )



        #
        # State
        #

        self.moves = []

        self.checks_given = 0

        self.training_active = False

        self.playing_color = "White"



        #
        # Signals
        #

        self.board.move_attempted.connect(
            self.handle_move_attempt
        )

        self.board.check_given.connect(
            self.player_check
        )



        #
        # Layout
        #

        right_panel = QVBoxLayout()

        right_panel.addWidget(
            self.opening_panel
        )

        right_panel.addStretch()


        layout.addLayout(
            info_panel,
            1
        )

        layout.addWidget(
            self.board,
            3
        )

        layout.addLayout(
            right_panel,
            1
        )


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



    def start_training(
        self,
        opening,
        variation,
        color
    ):

        self.training_active = True

        self.playing_color = color


        self.board.set_player_color(
            color
        )


        self.opening_manager.load_opening(
            opening,
            variation,
            color
        )


        self.board.reset_board()


        self.moves = []


        self.opening_label.setText(
            f"Opening: {variation}"
        )


        self.progress_label.setText(
            f"Progress: 0 / {len(self.opening_manager.moves)}"
        )


        self.status_label.setText(
            "Status: Training started"
        )


        self.history_label.setText(
            "Move History:\n"
        )


        self.update_history()



        #
        # If playing Black,
        # White makes the first opening move
        #

        if color == "Black":

            self.play_opening_move()



    def handle_move_attempt(
        self,
        san,
        move
    ):


        #
        # Opening training mode
        #

        if self.training_active:


            if self.board.board.turn != self.board.player_color:

                return



            if self.opening_manager.player_move_correct(
                san
            ):


                self.board.accept_move(
                    move
                )


                self.moves.append(
                    (
                        san,
                        ""
                    )
                )


                self.progress_label.setText(
                    f"Progress: {self.opening_manager.current_move} / {len(self.opening_manager.moves)}"
                )


                self.status_label.setText(
                    "Status: Correct move!"
                )


                self.update_history()


                self.play_opening_move()


            else:


                self.status_label.setText(
                    f"Incorrect move. Expected: {self.opening_manager.get_expected_move()}"
                )


            return



        #
        # Normal Stockfish mode
        #

        self.board.accept_move(
            move
        )


        self.moves.append(
            (
                san,
                ""
            )
        )


        self.update_history()


        self.play_stockfish_move()



    def play_opening_move(self):


        move_san = self.opening_manager.get_next_move()



        #
        # Opening completed
        #

        if move_san is None:


            self.training_active = False


            self.status_label.setText(
                "Opening complete. Stockfish activated."
            )


            #
            # If engine side to move
            #

            if self.board.board.turn != self.board.player_color:

                self.play_stockfish_move()


            return



        move = self.board.board.parse_san(
            move_san
        )


        self.board.make_engine_move(
            move
        )


        self.opening_manager.advance_trainer_move()


        self.moves.append(
            (
                "",
                move_san
            )
        )


        self.progress_label.setText(
            f"Progress: {self.opening_manager.current_move} / {len(self.opening_manager.moves)}"
        )


        self.update_history()



    def play_stockfish_move(self):

        if self.board.board.is_game_over():

            return


        self.status_label.setText(
            "Status: Stockfish thinking..."
        )


        engine_move = self.engine.get_move(
            self.board.board
        )


        if engine_move is None:

            return


        engine_san = self.board.board.san(
            engine_move
        )


        self.board.make_engine_move(
            engine_move
        )


        self.moves.append(
            (
                "",
                engine_san
            )
        )


        self.status_label.setText(
            "Status: Your turn"
        )


        self.update_history()



    def player_check(self):

        self.checks_given += 1


        self.engine.decrease_elo(
            100
        )


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



    def closeEvent(
        self,
        event
    ):

        self.engine.close()

        event.accept()