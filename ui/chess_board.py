from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtCore import Qt, Signal

import chess


class ChessBoard(QWidget):

    # Human completed a legal move
    move_made = Signal()

    # Human gave check
    check_given = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.board = chess.Board()

        self.selected_square = None
        self.legal_moves = []

        self.setMinimumSize(500, 500)

        self.light_square = QColor("#F0D9B5")
        self.dark_square = QColor("#B58863")

        self.highlight_color = QColor("#7FC97F")
        self.move_color = QColor("#B5E7A0")

        self.piece_font = QFont("Arial", 36)

    def paintEvent(self, event):

        painter = QPainter(self)

        board_size = min(
            self.width(),
            self.height()
        )

        square_size = board_size // 8

        painter.setFont(self.piece_font)
        painter.setPen(Qt.black)

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

        for row in range(8):

            for col in range(8):

                square = chess.square(
                    col,
                    7 - row
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

                # Selected square
                if square == self.selected_square:

                    painter.fillRect(
                        x,
                        y,
                        square_size,
                        square_size,
                        self.highlight_color
                    )

                # Legal destination squares
                if square in self.legal_moves:

                    painter.fillRect(
                        x,
                        y,
                        square_size,
                        square_size,
                        self.move_color
                    )

                # Draw piece
                piece = self.board.piece_at(square)

                if piece:

                    painter.drawText(
                        x,
                        y,
                        square_size,
                        square_size,
                        Qt.AlignCenter,
                        pieces[piece.symbol()]
                    )

    def mousePressEvent(self, event):

        board_size = min(
            self.width(),
            self.height()
        )

        square_size = board_size // 8

        col = int(event.position().x() // square_size)
        row = int(event.position().y() // square_size)

        if col > 7 or row > 7:
            return

        square = chess.square(
            col,
            7 - row
        )

        #
        # First click -> select white piece
        #

        if self.selected_square is None:

            piece = self.board.piece_at(square)

            if piece and piece.color == chess.WHITE:

                self.selected_square = square

                self.legal_moves = [
                    move.to_square
                    for move in self.board.legal_moves
                    if move.from_square == square
                ]

                self.update()

            return

        #
        # Second click -> attempt move
        #

        move = chess.Move(
            self.selected_square,
            square
        )

        if move in self.board.legal_moves:

            self.board.push(move)

            # Did this move give check?
            if self.board.is_check():
                self.check_given.emit()

            # Tell MainWindow that the player's move is complete
            self.move_made.emit()

        # Clear selection
        self.selected_square = None
        self.legal_moves = []

        self.update()

    def make_engine_move(self, move):
        """
        Apply Stockfish's move.
        """

        if move in self.board.legal_moves:

            self.board.push(move)

            self.update()