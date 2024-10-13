import socket
import threading

HEADER = 64
PORT = 1000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "D"
GAME_OVER_MESSAGE = "GAME_OVER"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
players = ['X', 'O']
board = [" " for _ in range(9)]  # Tic Tac Toe board

def send_message_to_client(conn, message):
    """Sends a length-prefixed message to the client."""
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def check_winner(mark):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == mark:
            return True
    return False

def board_full():
    return " " not in board

def handle_client(conn, addr):
    global clients
    if len(clients) >= 2:
        send_message_to_client(conn, "TOO_MANY_PLAYERS")
        conn.close()
        return

    player = players[len(clients)]  # Assign player based on current number of clients
    clients.append(conn)
    print(f"[NEW CONNECTION] {addr} connected as {player}.")
    
    send_message_to_client(conn, player)  # Send player identity ('X' or 'O')

    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT).strip()
            
            if msg_length == DISCONNECT_MESSAGE:
                print(f"[{addr}] {player} is disconnecting.")
                notify_disconnect(player)
                connected = False
                break
            
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"[{addr}] Message received: {msg}")
                
                if msg.startswith(player):
                    _, row, col = msg.split(':')
                    row, col = int(row), int(col)
                    index = row * 3 + col
                    board[index] = player
                    
                    for client in clients:
                        send_message_to_client(client, f"MOVE:{player}:{row}:{col}")
                    
                    if check_winner(player):
                        for client in clients:
                            send_message_to_client(client, f"WINNER:{player}")
                        reset_game()
                    elif board_full():
                        for client in clients:
                            send_message_to_client(client, "DRAW")
                        reset_game()

        except Exception as e:
            print(f"[ERROR] {e}")
            connected = False
            break
    
    print(f"[DISCONNECTED] {addr} disconnected.")
    clients.remove(conn)
    conn.close()

def notify_disconnect(disconnecting_player):
    index = players.index(disconnecting_player)
    other_player = players[1 - index]
    
    for client in clients:
        if players[clients.index(client)] == other_player:
            addr = client.getpeername()
            print(f"[NOTIFY DISCONNECT] Sending DISCONNECT message to {addr} ({other_player}).")
            send_message_to_client(client, "DISCONNECT")

def reset_game():
    global board
    print("[RESETTING GAME] Resetting the board for a new game.")
    board = [" " for _ in range(9)]
    
    for client in clients:
        send_message_to_client(client, "RESET_BOARD")

def start_server():
    server.listen()
    print(f"Server listening on {SERVER}")
    while True:
        if len(clients) < 2:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

start_server()
