from ui.engine import ChessEngine


engine = ChessEngine()

print(engine.get_elo())


engine.decrease_elo(500)

print(engine.get_elo())


engine.close()