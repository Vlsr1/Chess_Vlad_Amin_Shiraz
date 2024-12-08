import unittest
from chess_project.client import create_game, join_game, make_move, get_board

class TestClient(unittest.TestCase):
    def test_create_game(self):
        game_id = create_game()
        self.assertIsNotNone(game_id)

    def test_join_game(self):
        game_id = create_game()
        join_game(game_id)
        self.assertTrue(True)  # Заглушка для реального теста

    def test_make_move(self):
        game_id = create_game()
        make_move(game_id, 'e2e4')
        board = get_board(game_id)
        self.assertIsNotNone(board)

