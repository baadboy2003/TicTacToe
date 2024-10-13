import socket
import threading

# Constants
HEADER = 64  # Header size to define the length of each message
PORT = 1000  # Port on which the server listens
SERVER = socket.gethostbyname(socket.gethostname())  # Get the local machine's IP address
ADDR = (SERVER, PORT)  # Server's IP address and port tuple
FORMAT = 'utf-8'  # Encoding format for sending/receiving messages
DISCONNECT_MESSAGE = "D"  # Message used to signify a disconnection request
GAME_OVER_MESSAGE = "GAME_OVER"  # Message used to signify the game is over

# Initialize the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Lists to hold active client connections and the game state
clients = []
players = ['X', 'O']  # Two players in the game ('X' and 'O')
board = [" " for _ in range(9)]  # Tic-Tac-Toe board initialized with empty spaces

def send_message_to_client(conn, message):
    """
    Sends a length-prefixed message to the connected client.

    Args:
        conn (socket): The connection object for the client.
        message (str): The message to be sent.
    """
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # Pad the length to match the header size
    conn.send(send_length)
    conn.send(message)

def check_winner(mark):
    """
    Checks if the given player has won the game by comparing their moves 
    against all possible win conditions.

    Args:
        mark (str): The mark of the player ('X' or 'O').

    Returns:
        bool: True if the player has won, False otherwise.
    """
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
                      (0, 4, 8), (2, 4, 6)]  # Diagonal
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == mark:
            return True
    return False

def board_full():
    """
    Checks if the Tic-Tac-Toe board is full (i.e., no more empty spaces).

    Returns:
        bool: True if the board is full, False otherwise.
    """
    return " " not in board

def handle_client(conn, addr):
    """
    Handles communication with an individual client, including receiving moves, 
    broadcasting messages, and checking the game state.

    Args:
        conn (socket): The connection object for the client.
        addr (tuple): The address of the client (IP, port).
    """
    global clients
    player = players[len(clients)]  # Assign 'X' or 'O' based on the number of connected clients
    clients.append(conn)
    print(f"[NEW CONNECTION] {addr} connected as {player}.")
    
    send_message_to_client(conn, player)  # Send the player ID ('X' or 'O') to the client

    connected = True
    while connected:
        try:
            # Receive message length from the client
            msg_length = conn.recv(HEADER).decode(FORMAT).strip()
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                # If the client requests to disconnect
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    break

                print(f"[{addr}] {msg}")
                # Process player's move (e.g., "X:1:1" -> row: 1, col: 1)
                if msg.startswith(player):
                    _, row, col = msg.split(':')
                    row, col = int(row), int(col)
                    index = row * 3 + col
                    board[index] = player  # Update board with player's move
                    
                    # Broadcast the move to all clients
                    for client in clients:
                        send_message_to_client(client, f"MOVE:{player}:{row}:{col}")

                    # Check if the player has won or if it's a draw
                    if check_winner(player):
                        for client in clients:
                            send_message_to_client(client, f"WINNER:{player}")
                        reset_game()  # Reset the game after a win
                    elif board_full():
                        for client in clients:
                            send_message_to_client(client, "DRAW")
                        reset_game()  # Reset the game after a draw
        except Exception as e:
            print(f"[ERROR] {e}")
            connected = False
            break

    print(f"[DISCONNECTED] {addr} disconnected.")
    clients.remove(conn)
    conn.close()

    # Notify the other player about the disconnection and reset the game
    notify_disconnect(player)
    reset_game()

def notify_disconnect(disconnecting_player):
    """
    Notifies the other client that the player has disconnected.

    Args:
        disconnecting_player (str): The mark ('X' or 'O') of the disconnecting player.
    """
    for client in clients:
        if client != disconnecting_player:
            send_message_to_client(client, "DISCONNECT")

def reset_game():
    """
    Resets the game board and notifies all clients of the reset.
    """
    global board
    print("[RESETTING GAME] Resetting the board for a new game.")
    
    board = [" " for _ in range(9)]  # Reset the Tic-Tac-Toe board
    
    # Notify all clients that the board is being reset
    for client in clients:
        send_message_to_client(client, "RESET_BOARD")

def start_server():
    """
    Starts the server and listens for incoming client connections. 
    Spawns a new thread to handle each connected client.
    """
    server.listen()  # Start listening for incoming connections
    print(f"Server listening on {SERVER}")
    
    while True:
        if len(clients) < 2:  # Only allow up to 2 clients (for a 2-player game)
            conn, addr = server.accept()  # Accept a new connection
            thread = threading.Thread(target=handle_client, args=(conn, addr))  # Start a new thread to handle the client
            thread.start()  # Run the thread

# Start the server
start_server()
