class GameSettings:
    def __init__(self, player1, player2, time_control):
        self.player1 = player1
        self.player2 = player2
        self.time_control = time_control

    def to_dict(self):
        return {
            'player1': self.player1,
            'player2': self.player2,
            'time_control': self.time_control
        }

