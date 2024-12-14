import unittest
from chess_project.save_load import save_game, load_game
import chess

class TestSaveLoad(unittest.TestCase):
    def test_save_load_game(self):
        board = chess.Board()
        save_game(board, 'test_game.json')
        loaded_board = load_game('test_game.json')
        self.assertEqual(board.fen(), loaded_board.fen())

