
### Пример документации функции

#### game.py
```python
class ChessGame:
    """
    Класс для управления шахматной игрой.

    Атрибуты:
        board (chess.Board): Шахматная доска.

    Методы:
        make_move(move: str): Выполняет ход на доске.
        get_board_fen(): Возвращает FEN-строку текущего состояния доски.
    """
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move: str):
        """
        Выполняет ход на доске.

        Аргументы:
            move (str): Ход в формате SAN (Standard Algebraic Notation).
        """
        self.board.push_san(move)

    def get_board_fen(self) -> str:
        """
        Возвращает FEN-строку текущего состояния доски.

        Возвращает:
            str: FEN-строка.
        """
        return self.board.fen()

