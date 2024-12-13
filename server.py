import socket
import threading
import chess

# Серверные настройки
HOST = '0.0.0.0'
PORT = 65433

# Словарь для хранения игроков и их соединений
players = {}
current_game = chess.Board()

# Функция для обработки клиента
def handle_client(conn, addr, player_id):
    print(f"New connection from {addr}")
    players[player_id] = conn

    # Отправляем игроку его ID
    conn.sendall(f"Player {player_id}".encode())

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received from {addr}: {data.decode()}")

        # Обработка хода
        move = data.decode()
        try:
            current_game.push_san(move)
            print(f"Move {move} is valid")
        except ValueError:
            print(f"Move {move} is invalid")
            conn.sendall("Invalid move".encode())
            continue

        # Отправляем ход и обновленное состояние доски обоим игрокам
        board_str = str(current_game)
        for player_conn in players.values():
            player_conn.sendall(f"Move {move} by Player {player_id}\n{board_str}".encode())

    print(f"Connection from {addr} closed")
    conn.close()

# Запуск сервера
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server started on {HOST}:{PORT}")
        player_count = 0
        while player_count < 2:
            conn, addr = s.accept()
            player_count += 1
            threading.Thread(target=handle_client, args=(conn, addr, player_count)).start()

if __name__ == "__main__":
    start_server()