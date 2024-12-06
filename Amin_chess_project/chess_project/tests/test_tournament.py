import unittest
from chess_project.tournament import create_tournament, add_game_to_tournament, tournaments

class TestTournament(unittest.TestCase):
    def test_create_tournament(self):
        create_tournament(1)
        self.assertIn(1, tournaments)

    def test_add_game_to_tournament(self):
        create_tournament(1)
        add_game_to_tournament(1, 1)
        self.assertIn(1, tournaments[1])

