import chess.engine

def analyze_game(board):
    engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\Dlux\Desktop\stockfish")
    info = engine.analyse(board, chess.engine.Limit(time=2.0))
    print("Оценка:", info["score"])
    engine.quit()

