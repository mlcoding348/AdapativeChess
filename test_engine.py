import chess

from ui.engine import ChessEngine


engine = ChessEngine()

board = chess.Board()


print("Current board:")
print(board)


move = engine.get_move(board)


print("\nStockfish chooses:")
print(move)


engine.close()