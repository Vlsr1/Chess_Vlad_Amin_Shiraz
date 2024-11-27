import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 500, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

# Размеры клетки
CELL_SIZE = WIDTH // 8

# Цвета
WHITE = (236, 218, 185)
BLACK = (174, 138, 104)
GREEN = (0, 255, 0)

# Создание окна
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess")

# Загрузка изображений фигур
pieces = {
    'K': pygame.image.load('images/white_king.png'),
    'Q': pygame.image.load('images/white_queen.png'),
    'R': pygame.image.load('images/white_rook.png'),
    'B': pygame.image.load('images/white_bishop.png'),
    'N': pygame.image.load('images/white_knight.png'),
    'P': pygame.image.load('images/white_pawn.png'),
    'k': pygame.image.load('images/black_king.png'),
    'q': pygame.image.load('images/black_queen.png'),
    'r': pygame.image.load('images/black_rook.png'),
    'b': pygame.image.load('images/black_bishop.png'),
    'n': pygame.image.load('images/black_knight.png'),
    'p': pygame.image.load('images/black_pawn.png')
}

# Начальная позиция фигур
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# Логика передвижения фигур
def is_valid_move(piece, start, end):
    sx, sy = start
    ex, ey = end
    if piece == 'P':
        if sx == ex and sy == 6 and ey == 4:
            return True
        if sx == ex and sy - ey==1:
            return True
        if abs(sx - ex) == 1 and (sy - ey) == 1 and board[ey][ex]!=None:
            return True
    elif piece == 'p':
        if sx == ex and sy == 1 and ey == 3:
            return True
        if sx == ex and ey - sy == 1:
            return True
        if abs(sx - ex) == 1 and (ey - sy) == 1 and board[ey][ex]!=None:
            return True   
    elif piece in ['R', 'r']:
        if sx == ex or sy == ey:
            return True
    elif piece in ['B', 'b']:
        if abs(sx - ex) == abs(sy - ey):
            return True
    elif piece in ['N', 'n']:
        if (abs(sx - ex), abs(sy - ey)) in [(1, 2), (2, 1)]:
            return True
    elif piece in ['Q', 'q']:
        if sx == ex or sy == ey or abs(sx - ex) == abs(sy - ey):
            return True
    elif piece in ['K', 'k']:
        if abs(sx - ex) <= 1 and abs(sy - ey) <= 1:
            return True
    return False

def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                screen.blit(pieces[piece], (col * CELL_SIZE, row * CELL_SIZE))

def main():
    selected_piece = None
    selected_pos = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // CELL_SIZE, y // CELL_SIZE
                if selected_piece is None:
                    if board[row][col]:
                        selected_piece = board[row][col]
                        selected_pos = (col, row)
                else:
                    if is_valid_move(selected_piece, selected_pos, (col, row)):
                        board[row][col] = selected_piece
                        board[selected_pos[1]][selected_pos[0]] = None
                    selected_piece = None
                    selected_pos = None

        screen.fill(WHITE)
        draw_board()
        draw_pieces()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()