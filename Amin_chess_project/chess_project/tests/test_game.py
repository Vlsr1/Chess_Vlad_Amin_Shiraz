import unittest
from chess_project.game import ChessGame

class TestGame(unittest.TestCase):
    def test_make_move(self):
        game = ChessGame()
        game.make_move('e2e4')
        self.assertEqual(game.get_board_fen(), 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')

