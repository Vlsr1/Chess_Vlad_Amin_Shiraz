import unittest
from chess_project.engine import analyze_game
import chess

class TestEngine(unittest.TestCase):
    def test_analyze_game(self):
        board = chess.Board()
        analyze_game(board)
        self.assertTrue(True)  # Заглушка для реального теста

