import chess

class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move):
        self.board.push_san(move)

    def get_board_fen(self):
        return self.board.fen()

