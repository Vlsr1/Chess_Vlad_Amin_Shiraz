import json

def save_game(board, filename):
    with open(filename, 'w') as file:
        json.dump(board.fen(), file)

def load_game(filename):
    with open(filename, 'r') as file:
        board_fen = json.load(file)
        return chess.Board(board_fen)

