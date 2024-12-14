import chess.pgn
import chess.engine
import os
import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 500, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

# Размеры клетки
CELL_SIZE = WIDTH // 8

# Алфавит
alph = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')

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

def load_pgn_file(pgn_file):
    with open(pgn_file) as pgn:
        return chess.pgn.read_game(pgn)

def initialize_engine(engine_path):
    return chess.engine.SimpleEngine.popen_uci(engine_path)

def analyze_pgn(pgn_file, engine_path, depth):
    game = load_pgn_file(pgn_file)
    engine = initialize_engine(engine_path)
    board = game.board()
    move_number = 1
    move_info = []

    for move in game.mainline_moves():
        piece_name = chess.piece_name(board.piece_type_at(move.from_square))
        board.push(move)
        info = engine.analyse(board, chess.engine.Limit(depth=depth))
        score = info["score"].relative.score() / 100.0
        if not board.turn:
            score = -score
        advantage = 'Equal' if -0.3 < score < 0.3 else 'White' if score > 0 else 'Black'
        move_info.append((move_number, piece_name, move, score, advantage))
        if not board.turn:
            move_number += 1

    engine.quit()
    return move_info

def print_move_info(move_info):
    for info in move_info:
        move_number, piece_name, move, score, advantage = info
        print(f"Move {move_number}: {piece_name} {move}, Score: {score:.2f}, Advantage: {advantage}")

def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                screen.blit(pieces[piece.symbol()], (col * CELL_SIZE, row * CELL_SIZE))

def draw_arrow(start_square, end_square):
    start_col, start_row = chess.square_file(start_square), 7 - chess.square_rank(start_square)
    end_col, end_row = chess.square_file(end_square), 7 - chess.square_rank(end_square)
    start_pos = (start_col * CELL_SIZE + CELL_SIZE // 2, start_row * CELL_SIZE + CELL_SIZE // 2)
    end_pos = (end_col * CELL_SIZE + CELL_SIZE // 2, end_row * CELL_SIZE + CELL_SIZE // 2)

    pygame.draw.line(screen, GREEN, start_pos, end_pos, 5)
    arrow_length = 20
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
    arrow_head = (
        end_pos[0] - arrow_length * math.cos(angle - math.pi / 6),
        end_pos[1] - arrow_length * math.sin(angle - math.pi / 6)
    )
    pygame.draw.polygon(screen, GREEN, [end_pos, arrow_head, (end_pos[0] - arrow_length * math.cos(angle + math.pi / 6), end_pos[1] - arrow_length * math.sin(angle + math.pi / 6))])

def show_position_and_best_move(engine_path, move_info, depth):
    engine = initialize_engine(engine_path)
    while True:
        move_number = int(input("Введите номер хода для отображения позиции и лучшего хода: "))
        for info in move_info:
            if info[0] == move_number:
                move_number, piece_name, move, score, advantage = info
                board = chess.Board()
                for m in move_info[:move_info.index(info)]:
                    board.push(m[2])
                board.push(move)
                print(f"Position after move {move_number}:")

                screen.fill(WHITE)
                draw_board()
                draw_pieces(board)
                pygame.display.flip()

                info = engine.analyse(board, chess.engine.Limit(depth=depth))
                best_move = info["pv"][0]
                print(f"Best move: {best_move}")

                draw_arrow(best_move.from_square, best_move.to_square)
                pygame.display.flip()

                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False

                choice = input("Введите 'new' для выбора другого PGN файла, 'move' для выбора другого хода или 'exit' для выхода: ").strip().lower()
                if choice == 'new':
                    engine.quit()
                    return
                elif choice == 'move':
                    break
                elif choice == 'exit':
                    engine.quit()
                    pygame.quit()
                    sys.exit()
                else:
                    print("Неверный ввод. Пожалуйста, попробуйте снова.")

def main():
    while True:
        pgn_filename = input("Введите название PGN файла (без расширения) или 'exit' для выхода: ")
        if pgn_filename.lower() == 'exit':
            break
        pgn_file = os.path.join(os.path.dirname(__file__), 'pgn', f"{pgn_filename}.pgn")

        if not os.path.exists(pgn_file):
            print(f"Файл {pgn_file} не найден.")
        else:
            engine_path = "stockfish"
            if not os.access(engine_path, os.X_OK):
                print(f"Permission denied: {engine_path}")
                print("Please ensure the Stockfish engine has execute permissions.")
            else:
                depth = int(input("Введите глубину анализа (например, 15): "))
                move_info = analyze_pgn(pgn_file, engine_path, depth)
                print_move_info(move_info)
                show_position_and_best_move(engine_path, move_info, depth)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()