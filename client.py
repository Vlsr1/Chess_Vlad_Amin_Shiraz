import socket

# Клиентские настройки
HOST = '127.0.0.1'
PORT = 65433

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        player_id = s.recv(1024).decode()
        print(f"Connected as {player_id}")

        while True:
            move = input("Enter your move: ")
            s.sendall(move.encode())
            data = s.recv(1024)
            print(f"Received from server:\n{data.decode()}")

if __name__ == "__main__":
    start_client()