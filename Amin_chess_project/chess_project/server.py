import socket
import threading
import json
import chess
import signal
import sys

HOST = '127.0.0.1'
PORT = 65435  # Измененный порт
games = {}

def handle_client(conn, addr):
    print(f"Подключено {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            request = json.loads(data.decode('utf-8'))
            response = process_request(request)
            conn.sendall(json.dumps(response).encode('utf-8'))
        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            break
    conn.close()

def process_request(request):
    action = request.get('action')
    if action == 'create_game':
        game_id = create_game()
        return {'status': 'success', 'game_id': game_id}
    elif action == 'join_game':
        game_id = request.get('game_id')
        join_game(game_id)
        return {'status': 'success'}
    elif action == 'make_move':
        game_id = request.get('game_id')
        move = request.get('move')
        make_move(game_id, move)
        return {'status': 'success'}
    elif action == 'get_board':
        game_id = request.get('game_id')
        board = get_board(game_id)
        return {'status': 'success', 'board': board}
    else:
        return {'status': 'error', 'message': 'Неверное действие'}

def create_game():
    game_id = len(games) + 1
    games[game_id] = chess.Board()
    return game_id

def join_game(game_id):
    if game_id in games:
        pass

def make_move(game_id, move):
    if game_id in games:
        board = games[game_id]
        board.push_san(move)

def get_board(game_id):
    if game_id in games:
        board = games[game_id]
        return board.fen()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен на {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

def signal_handler(sig, frame):
    print('Завершение работы сервера...')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    start_server()

