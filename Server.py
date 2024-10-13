import socket
import threading

# Constants
HEADER = 64  # Fixed size for the length of the incoming message
PORT = 1000  # Port for the server to listen on
SERVER = socket.gethostbyname(socket.gethostname())  # Get the IP address of the local machine
ADDR = (SERVER, PORT)  # Server address
FORMAT = 'utf-8'  # Format for encoding/decoding messages
DISCONNECT_MESSAGE = "D"  # Message to indicate a client wants to disconnect
GAME_OVER_MESSAGE = "GAME_OVER"  # Message to indicate the game is over

# Setup the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []  # List to store connected clients
players = ['X', 'O']  # Players are 'X' and 'O'
board = [" " for _ in range(9)]  # Tic-Tac-Toe board represented as a list of 9 spaces

def send_message_to_client(conn, message):
    """Sends a length-prefixed message to the client.
    
    Args:
        conn: The client socket connection.
        message: The message string to send to the client.
    """
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # Padding to meet the HEADER size
    conn.send(send_length)
    conn.send(message)

def check_winner(mark):
    """Check if a player has won by matching their mark on the board.
    
    Args:
        mark: The player's mark ('X' or 'O').
    
    Returns:
        bool: True if the player has won, False otherwise.
    """
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal win conditions
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical win conditions
                      (0, 4, 8), (2, 4, 6)]  # Diagonal win conditions
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == mark:
            return True
    return False

def board_full():
    """Check if the Tic-Tac-Toe board is full (i.e., no more moves left).
    
    Returns:
        bool: True if the board is full, False otherwise.
    """
    return " " not in board

def handle_client(conn, addr):
    """Handle the interaction with a connected client.
    
    Args:
        conn: The client socket connection.
        addr: The address of the client.
    """
    global clients
    if len(clients) >= 2:
        send_message_to_client(conn, "TOO_MANY_PLAYERS")  # Reject connection if there are already 2 players
        conn.close()
        return

    player = players[len(clients)]  # Assign 'X' or 'O' based on the current number of connected clients
    clients.append(conn)  # Add the client to the list
    print(f"[NEW CONNECTION] {addr} connected as {player}.")
    
    send_message_to_client(conn, player)  # Inform the client of their role ('X' or 'O')

    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT).strip()  # Receive the length of the incoming message
            
            if msg_length == DISCONNECT_MESSAGE:
                print(f"[{addr}] {player} is disconnecting.")
                notify_disconnect(player)  # Notify the other player of the disconnection
                connected = False
                break
            
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)  # Receive the actual message
                print(f"[{addr}] Message received: {msg}")
                
                if msg.startswith(player):  # Ensure the message is from the correct player
                    _, row, col = msg.split(':')
                    row, col = int(row), int(col)
                    index = row * 3 + col  # Convert the row and col to a board index
                    board[index] = player  # Update the board
                    
                    # Send the move to both players
                    for client in clients:
                        send_message_to_client(client, f"MOVE:{player}:{row}:{col}")
                    
                    # Check for a winner or if the board is full
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
    clients.remove(conn)  # Remove the client from the list upon disconnection
    conn.close()

def notify_disconnect(disconnecting_player):
    """Notify the remaining player that their opponent has disconnected.
    
    Args:
        disconnecting_player: The player ('X' or 'O') who is disconnecting.
    """
    index = players.index(disconnecting_player)
    other_player = players[1 - index]  # Get the other player
    
    for client in clients:
        if players[clients.index(client)] == other_player:
            addr = client.getpeername()
            print(f"[NOTIFY DISCONNECT] Sending DISCONNECT message to {addr} ({other_player}).")
            send_message_to_client(client, "DISCONNECT")  # Notify the other player

def reset_game():
    """Reset the game board for a new game."""
    global board
    print("[RESETTING GAME] Resetting the board for a new game.")
    board = [" " for _ in range(9)]  # Clear the board
    
    for client in clients:
        send_message_to_client(client, "RESET_BOARD")  # Notify clients that the board has been reset

def start_server():
    """Start the server and handle incoming connections."""
    server.listen()
    print(f"Server listening on {SERVER}")
    while True:
        if len(clients) < 2:  # Only accept connections if fewer than 2 players are connected
            conn, addr = server.accept()  # Accept incoming connections
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()  # Start a new thread for each client connection
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  # Display active connections

# Start the server
start_server()
