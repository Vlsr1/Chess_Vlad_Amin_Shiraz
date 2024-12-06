import socket
import json
import pygame
import chess

HOST = '127.0.0.1'
PORT = 65435  # Измененный порт

def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(request).encode('utf-8'))
        data = s.recv(1024)
        return json.loads(data.decode('utf-8'))

def create_game():
    request = {'action': 'create_game'}
    response = send_request(request)
    if response['status'] == 'success':
        return response['game_id']
    else:
        print("Ошибка создания игры")
        return None

def join_game(game_id):
    request = {'action': 'join_game', 'game_id': game_id}
    response = send_request(request)
    if response['status'] == 'success':
        print("Присоединено к игре")
    else:
        print("Ошибка присоединения к игре")

def make_move(game_id, move):
    request = {'action': 'make_move', 'game_id': game_id, 'move': move}
    response = send_request(request)
    if response['status'] == 'success':
        print("Ход сделан")
    else:
        print("Ошибка при выполнении хода")

def get_board(game_id):
    request = {'action': 'get_board', 'game_id': game_id}
    response = send_request(request)
    if response['status'] == 'success':
        return response['board']
    else:
        print("Ошибка получения доски")
        return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('Шахматы')

    game_id = create_game()
    join_game(game_id)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

        board_fen = get_board(game_id)
        if board_fen:
            board = chess.Board(board_fen)
            draw_board(screen, board)

        pygame.display.flip()

    pygame.quit()

def draw_board(screen, board):
    pass

if __name__ == "__main__":
    main()

