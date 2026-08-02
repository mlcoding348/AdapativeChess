from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtCore import Qt, Signal

import chess


class ChessBoard(QWidget):

    move_attempted = Signal(str, chess.Move)

    move_made = Signal(str)

    check_given = Signal()


    def __init__(self, parent=None):

        super().__init__(parent)


        self.board = chess.Board()


        self.selected_square = None

        self.legal_moves = []


        self.player_color = chess.WHITE


        self.setMinimumSize(
            500,
            500
        )


        self.light_square = QColor("#F0D9B5")

        self.dark_square = QColor("#B58863")


        self.highlight_color = QColor("#7FC97F")

        self.move_color = QColor("#B5E7A0")


        self.piece_font = QFont(
            "Segoe UI Symbol",
            36
        )



    def set_player_color(
        self,
        color
    ):

        if color == "Black":

            self.player_color = chess.BLACK

        else:

            self.player_color = chess.WHITE


        self.update()



    def reset_board(self):

        self.board = chess.Board()

        self.selected_square = None

        self.legal_moves = []

        self.update()



    def get_square(
        self,
        row,
        col
    ):

        if self.player_color == chess.WHITE:

            return chess.square(
                col,
                7-row
            )

        else:

            return chess.square(
                7-col,
                row
            )



    def paintEvent(
        self,
        event
    ):

        painter = QPainter(self)


        size = min(
            self.width(),
            self.height()
        )


        square_size = size // 8


        pieces = {

            "K": "♔",
            "Q": "♕",
            "R": "♖",
            "B": "♗",
            "N": "♘",
            "P": "♙",

            "k": "♚",
            "q": "♛",
            "r": "♜",
            "b": "♝",
            "n": "♞",
            "p": "♟",
        }


        painter.setFont(
            self.piece_font
        )

        painter.setPen(
            Qt.black
        )


        for row in range(8):

            for col in range(8):


                square = self.get_square(
                    row,
                    col
                )


                x = col * square_size

                y = row * square_size


                color = (

                    self.light_square

                    if (row + col) % 2 == 0

                    else self.dark_square

                )


                painter.fillRect(
                    x,
                    y,
                    square_size,
                    square_size,
                    color
                )


                if square == self.selected_square:

                    painter.fillRect(
                        x,
                        y,
                        square_size,
                        square_size,
                        self.highlight_color
                    )


                if square in self.legal_moves:

                    painter.fillRect(
                        x,
                        y,
                        square_size,
                        square_size,
                        self.move_color
                    )


                piece = self.board.piece_at(
                    square
                )


                if piece:

                    painter.drawText(
                        x,
                        y,
                        square_size,
                        square_size,
                        Qt.AlignCenter,
                        pieces[piece.symbol()]
                    )



    def mousePressEvent(
        self,
        event
    ):

        size = min(
            self.width(),
            self.height()
        )


        square_size = size // 8


        col = int(
            event.position().x()
            //
            square_size
        )


        row = int(
            event.position().y()
            //
            square_size
        )


        if row > 7 or col > 7:

            return



        square = self.get_square(
            row,
            col
        )



        if self.selected_square is None:


            piece = self.board.piece_at(
                square
            )


            if piece and piece.color == self.player_color:


                self.selected_square = square


                self.legal_moves = [

                    move.to_square

                    for move in self.board.legal_moves

                    if move.from_square == square

                ]


                self.update()


            return



        move = chess.Move(
            self.selected_square,
            square
        )


        if move in self.board.legal_moves:


            san = self.board.san(
                move
            )


            self.move_attempted.emit(
                san,
                move
            )



        self.selected_square = None

        self.legal_moves = []

        self.update()



    def accept_move(
        self,
        move
    ):

        san = self.board.san(
            move
        )


        self.board.push(
            move
        )


        if self.board.is_check():

            self.check_given.emit()



        self.move_made.emit(
            san
        )


        self.update()



    def make_engine_move(
        self,
        move
    ):

        self.board.push(
            move
        )

        self.update()