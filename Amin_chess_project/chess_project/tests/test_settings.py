import unittest
from chess_project.settings import GameSettings

class TestSettings(unittest.TestCase):
    def test_to_dict(self):
        settings = GameSettings('Игрок1', 'Игрок2', '5+3')
        settings_dict = settings.to_dict()
        self.assertEqual(settings_dict, {
            'player1': 'Игрок1',
            'player2': 'Игрок2',
            'time_control': '5+3'
        })

if __name__ == '__main__':
    unittest.main()

