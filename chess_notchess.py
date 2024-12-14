import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 500, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

# Размеры клетки
CELL_SIZE = WIDTH // 8


# Алфавит
alph = ("a", "b", "c", "d", "e", "f", "g", "h")


WHITE = (236, 218, 185)
BLACK = (174, 138, 104)
GREEN = (0, 255, 0)

# Создание окна
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess")

# Загрузка изображений фигур
pieces = {
    "K": pygame.image.load("images/white_king.png"),
    "Q": pygame.image.load("images/white_queen.png"),
    "R": pygame.image.load("images/white_rook.png"),
    "B": pygame.image.load("images/white_bishop.png"),
    "N": pygame.image.load("images/white_knight.png"),
    "P": pygame.image.load("images/white_pawn.png"),
    "k": pygame.image.load("images/black_king.png"),
    "q": pygame.image.load("images/black_queen.png"),
    "r": pygame.image.load("images/black_rook.png"),
    "b": pygame.image.load("images/black_bishop.png"),
    "n": pygame.image.load("images/black_knight.png"),
    "p": pygame.image.load("images/black_pawn.png"),
}

# Начальная позиция фигур
board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]

# Логика передвижения фигур

k = []
last_double_pawn_move = (
    None  # Will store (x, y) of the pawn that just moved two squares
)
white_king_moved = False
black_king_moved = False
white_rooks_moved = [False, False]  # [queenside, kingside]
black_rooks_moved = [False, False]  # [queenside, kingside]


def get_king_position(side):
    """Find the position of the king for the given side."""
    king = "K" if side == "WHITE" else "k"
    for y in range(8):
        for x in range(8):
            if board[y][x] == king:
                return (x, y)
    return None


def is_square_attacked(square, by_side):
    """Check if a square is attacked by any piece of the given side."""
    x, y = square
    attacking_side = "BLACK" if by_side == "WHITE" else "WHITE"

    # Check all squares for enemy pieces that could attack this square
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None:
                # Only check pieces of the attacking side
                if (piece.islower() and by_side == "BLACK") or (
                    piece.isupper() and by_side == "WHITE"
                ):
                    # Temporarily remove piece on target square to check attack paths
                    temp = board[y][x]
                    board[y][x] = None
                    if is_valid_move(piece, (col, row), (x, y), attacking_side):
                        board[y][x] = temp
                        return True
                    board[y][x] = temp
    return False


def is_in_check(side):
    """Check if the given side's king is in check."""
    king_pos = get_king_position(side)
    if king_pos is None:
        return False
    return is_square_attacked(king_pos, "BLACK" if side == "WHITE" else "WHITE")


def get_piece_moves(piece, start, side):
    """Get all valid moves for a piece."""
    sx, sy = start
    moves = []
    for y in range(8):
        for x in range(8):
            if is_valid_move(piece, (sx, sy), (x, y), side):
                moves.append((x, y))
    return moves


def is_pinned(piece_pos, side):
    """Check if a piece is pinned to its king."""
    x, y = piece_pos
    piece = board[y][x]
    if piece is None:
        return False

    king_pos = get_king_position(side)
    if king_pos is None:
        return False

    kx, ky = king_pos

    # If piece is not in line with king (horizontally, vertically, or diagonally),
    # it cannot be pinned
    if not (x == kx or y == ky or abs(x - kx) == abs(y - ky)):
        return False

    # Get the direction from king to piece
    dx = 0 if x == kx else (x - kx) // abs(x - kx)
    dy = 0 if y == ky else (y - ky) // abs(y - ky)

    # Check if there are any pieces between king and our piece
    cx, cy = kx + dx, ky + dy
    while (cx, cy) != (x, y):
        if board[cy][cx] is not None:
            return False  # Another piece blocks the pin
        cx += dx
        cy += dy

    # Look beyond our piece for an attacking piece
    cx, cy = x + dx, y + dy
    while 0 <= cx < 8 and 0 <= cy < 8:
        if board[cy][cx] is not None:
            # Check if it's an enemy piece that could pin us
            enemy = board[cy][cx]
            if piece.isupper() == enemy.isupper():
                return False  # Same color piece

            # Check if it's a piece that can pin (queen, rook for orthogonal, bishop for diagonal)
            if dx == 0 or dy == 0:  # Orthogonal pin
                return enemy.lower() in ["r", "q"]
            else:  # Diagonal pin
                return enemy.lower() in ["b", "q"]
        cx += dx
        cy += dy

    return False


def move_escapes_check(piece, start, end, side):
    """Check if a move gets the king out of check or maintains a pin."""
    sx, sy = start
    ex, ey = end

    # If piece is pinned, only allow moves along the pin line
    if is_pinned((sx, sy), side):
        king_pos = get_king_position(side)
        kx, ky = king_pos

        # Check if move stays in line with king
        if sx == kx:  # Vertical pin
            if ex != kx:
                return False
        elif sy == ky:  # Horizontal pin
            if ey != ky:
                return False
        else:  # Diagonal pin
            if abs(ex - kx) != abs(ey - ky):
                return False
            if (ex - kx) * (sx - kx) <= 0:  # Can't move past king
                return False

    # Make temporary move
    temp_target = board[ey][ex]
    temp_start = board[sy][sx]
    board[ey][ex] = temp_start
    board[sy][sx] = None

    # Check if king is in check after move
    still_in_check = is_in_check(side)

    # Restore board
    board[sy][sx] = temp_start
    board[ey][ex] = temp_target

    return not still_in_check


def is_valid_move(piece, start, end, side):
    sx, sy = start
    ex, ey = end

    # First check basic move validity
    if not is_basic_valid_move(piece, start, end, side):
        return False

    # Check if piece is pinned
    if is_pinned((sx, sy), side):
        # Only allow moves that keep protecting the king
        if not move_escapes_check(piece, start, end, side):
            return False

    # If king is in check, only allow moves that escape check
    if is_in_check(side):
        if not move_escapes_check(piece, start, end, side):
            return False

    # For king moves, ensure destination square is not attacked
    if piece in ["K", "k"]:
        enemy_side = "BLACK" if side == "WHITE" else "WHITE"
        if is_square_attacked((ex, ey), enemy_side):
            return False

        # For castling, check additional squares for attacks
        if abs(sx - ex) == 2:
            # Check squares the king moves through
            step = 1 if ex > sx else -1
            if is_square_attacked((sx + step, sy), enemy_side):
                return False

    return True


# Rename the existing move validation logic to is_basic_valid_move
def is_basic_valid_move(piece, start, end, side):
    global last_double_pawn_move
    sx, sy = start
    ex, ey = end

    if (piece.islower() and side == "WHITE") or (
        not piece.islower() and side == "BLACK"
    ):
        return False
    if sx == ex and sy == ey:
        return False

    # White pawn movement
    if piece == "P":
        if side == "BLACK":
            return False
        # Normal one square forward
        if sx == ex and sy - ey == 1 and board[ey][ex] is None:
            return True
        # Initial two square move
        if (
            sx == ex
            and sy == 6
            and ey == 4
            and board[5][ex] is None
            and board[4][ex] is None
        ):
            return True
        # Normal capture
        if (
            abs(sx - ex) == 1
            and sy - ey == 1
            and board[ey][ex] is not None
            and board[ey][ex].islower()
        ):
            return True
        # En passant capture
        if abs(sx - ex) == 1 and sy - ey == 1 and board[ey][ex] is None:
            if last_double_pawn_move == (ex, ey + 1) and board[ey + 1][ex] == "p":
                return True
        return False

    # Black pawn movement
    elif piece == "p":
        if side == "WHITE":
            return False
        # Normal one square forward
        if sx == ex and ey - sy == 1 and board[ey][ex] is None:
            return True
        # Initial two square move
        if (
            sx == ex
            and sy == 1
            and ey == 3
            and board[2][ex] is None
            and board[3][ex] is None
        ):
            return True
        # Normal capture
        if (
            abs(sx - ex) == 1
            and ey - sy == 1
            and board[ey][ex] is not None
            and not board[ey][ex].islower()
        ):
            return True
        # En passant capture
        if abs(sx - ex) == 1 and ey - sy == 1 and board[ey][ex] is None:
            if last_double_pawn_move == (ex, ey - 1) and board[ey - 1][ex] == "P":
                return True
        return False

    elif piece in ["R", "r"]:
        if sx == ex:
            step = 1 if ey > sy else -1
            for y in range(sy + step, ey, step):
                if board[y][sx] is not None:  # Check for obstacles
                    return False
            else:
                if board[ey][ex] is None:
                    return True
                else:
                    print("fuck me")
                    if board[ey][ex].islower() != piece.islower():
                        return True
        if sy == ey:
            step = 1 if ex > sx else -1
            for x in range(sx + step, ex, step):
                if board[sy][x] is not None:  # Check for obstacles
                    return False
            else:
                if board[ey][ex] is None:
                    return True
                else:
                    print("fuck me")
                    if board[ey][ex].islower() != piece.islower():
                        return True
        return False

    elif piece in ["B", "b"]:
        if abs(ex - sx) == abs(ey - sy):  # Diagonal movement
            step_x = 1 if ex > sx else -1
            step_y = 1 if ey > sy else -1
            x, y = sx + step_x, sy + step_y
            while (x, y) != (ex, ey):
                if board[y][x] is not None:  # Check for obstacles
                    return False
                x += step_x
                y += step_y
            else:
                if board[y][x] is None:
                    return True
                else:
                    print("fuck me")
                    if board[y][x].islower() != piece.islower():
                        return True
        return False

    elif piece in ["Q", "q"]:
        if sx == ex or sy == ey:  # Rook-like movement
            if piece == "Q":
                return is_basic_valid_move("R", (sx, sy), (ex, ey), side)
            else:
                return is_basic_valid_move("r", (sx, sy), (ex, ey), side)
        elif abs(ex - sx) == abs(ey - sy):  # Bishop-like movement
            if piece == "Q":
                return is_basic_valid_move("B", (sx, sy), (ex, ey), side)
            else:
                return is_basic_valid_move("b", (sx, sy), (ex, ey), side)

    elif piece in ["N", "n"]:
        if (abs(sx - ex), abs(sy - ey)) in [(1, 2), (2, 1)]:
            if board[ey][ex] is None:
                return True
            elif (board[ey][ex] is not None) and board[ey][
                ex
            ].islower() != piece.islower():
                return True
            else:
                print("fuck me")
        return False

    elif piece in ["K", "k"]:
        # Normal king movement
        if abs(sx - ex) <= 1 and abs(sy - ey) <= 1:
            if board[ey][ex] is None:
                return True
            elif board[ey][ex].islower() != piece.islower():
                return True

        # Castling
        if sy == ey and abs(sx - ex) == 2:
            # White king castling
            if piece == "K" and sy == 7:
                if not white_king_moved:
                    # Kingside castling
                    if ex == 6 and not white_rooks_moved[1]:
                        if all(board[7][i] is None for i in range(5, 7)):
                            return True
                    # Queenside castling
                    elif ex == 2 and not white_rooks_moved[0]:
                        if all(board[7][i] is None for i in range(1, 4)):
                            return True
            # Black king castling
            elif piece == "k" and sy == 0:
                if not black_king_moved:
                    # Kingside castling
                    if ex == 6 and not black_rooks_moved[1]:
                        if all(board[0][i] is None for i in range(5, 7)):
                            return True
                    # Queenside castling
                    elif ex == 2 and not black_rooks_moved[0]:
                        if all(board[0][i] is None for i in range(1, 4)):
                            return True
        return False


def draw_board(selected_piece=None, selected_pos=None, side=None):
    for row in range(8):
        for col in range(8):
            # Draw base board squares
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(
                screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

            # If a piece is selected, show possible moves
            if selected_piece:
                if is_valid_move(selected_piece, selected_pos, (col, row), side):
                    square_rect = pygame.Rect(
                        col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE
                    )

                    if board[row][col] is None:  # Empty square - show green circle
                        # Draw semi-transparent green overlay
                        s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                        pygame.draw.circle(
                            s,
                            (0, 255, 0, 64),
                            (CELL_SIZE // 2, CELL_SIZE // 2),
                            CELL_SIZE // 3,
                        )
                        screen.blit(s, square_rect)
                    else:  # Capture square - show red border
                        if board[row][col].islower() != selected_piece.islower():
                            pygame.draw.rect(screen, (255, 0, 0), square_rect, 3)
                            # Draw semi-transparent red overlay
                            s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                            pygame.draw.rect(s, (255, 0, 0, 32), s.get_rect())
                            screen.blit(s, square_rect)

            # Highlight selected piece's square
            if selected_pos == (col, row):
                pygame.draw.rect(
                    screen,
                    (0, 128, 255),  # Blue color for selected piece
                    (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    3,
                )


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

    pgn = ()
    move_number = int(1)
    side = "WHITE"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // CELL_SIZE, y // CELL_SIZE

                if selected_piece is None:
                    if board[row][col]:
                        # Only allow selecting pieces of current side
                        piece = board[row][col]
                        if (piece.isupper() and side == "WHITE") or (
                            piece.islower() and side == "BLACK"
                        ):
                            selected_piece = piece
                            selected_pos = (col, row)
                else:
                    if is_valid_move(selected_piece, selected_pos, (col, row), side):
                        # Store the previous position
                        old_row = selected_pos[1]
                        old_col = selected_pos[0]

                        # Track king and rook movements for castling
                        if selected_piece == "K":
                            global white_king_moved
                            white_king_moved = True
                            # Handle castling move
                            if abs(old_col - col) == 2:
                                # Kingside castling
                                if col == 6:
                                    board[7][5] = board[7][7]  # Move rook
                                    board[7][7] = None
                                # Queenside castling
                                elif col == 2:
                                    board[7][3] = board[7][0]  # Move rook
                                    board[7][0] = None
                        elif selected_piece == "k":
                            global black_king_moved
                            black_king_moved = True
                            # Handle castling move
                            if abs(old_col - col) == 2:
                                # Kingside castling
                                if col == 6:
                                    board[0][5] = board[0][7]  # Move rook
                                    board[0][7] = None
                                # Queenside castling
                                elif col == 2:
                                    board[0][3] = board[0][0]  # Move rook
                                    board[0][0] = None
                        # Track rook movements
                        elif selected_piece == "R":
                            if old_row == 7:
                                if old_col == 0:
                                    white_rooks_moved[0] = True
                                elif old_col == 7:
                                    white_rooks_moved[1] = True
                        elif selected_piece == "r":
                            if old_row == 0:
                                if old_col == 0:
                                    black_rooks_moved[0] = True
                                elif old_col == 7:
                                    black_rooks_moved[1] = True

                        # Check for en passant capture
                        if (
                            selected_piece in ["P", "p"]
                            and abs(selected_pos[0] - col) == 1
                            and board[row][col] is None
                        ):
                            # Remove the captured pawn
                            if selected_piece == "P":
                                board[row + 1][col] = None
                            else:
                                board[row - 1][col] = None

                        # Make the move
                        board[row][col] = selected_piece
                        board[old_row][selected_pos[0]] = None

                        # Track double pawn moves
                        global last_double_pawn_move
                        if selected_piece == "P" and old_row == 6 and row == 4:
                            last_double_pawn_move = (col, row)
                        elif selected_piece == "p" and old_row == 1 and row == 3:
                            last_double_pawn_move = (col, row)
                        else:
                            last_double_pawn_move = None

                        # Switch sides
                        side = "BLACK" if side == "WHITE" else "WHITE"

                    selected_piece = None
                    selected_pos = None

        screen.fill(WHITE)
        draw_board(selected_piece, selected_pos, side)
        draw_pieces()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

    print(pgn)


if __name__ == "__main__":
    main()

    main()
