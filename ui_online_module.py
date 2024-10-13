import socket
import threading
import tkinter as tk
from ui_base_module import TicTacToeBaseUI

PORT = 1000  # Port used for the server connection
SERVER = socket.gethostbyname(socket.gethostname())  # Gets the IP of the local machine
ADDR = (SERVER, PORT)  # Combines server IP and port into a tuple
FORMAT = 'utf-8'  # Encoding format for sending and receiving messages
HEADER = 64  # The size of the message header to specify message length
DISCONNECT_MESSAGE = "D"  # Message sent to the server to signal disconnection
GAME_OVER_MESSAGE = "GAME_OVER"  # Message sent when the game is over

class TicTacToeOnlineUI(TicTacToeBaseUI):
    """
    The TicTacToeOnlineUI class is responsible for handling the online multiplayer UI 
    and server communication for the Tic-Tac-Toe game. It allows players to connect to 
    a server, send and receive game moves, and manage game flow.
    
    Attributes:
        client (socket): The client socket used to communicate with the server.
        player (str): Indicates whether the player is 'X' or 'O'.
        turn (bool): Boolean flag to indicate if it's the player's turn.
        game_in_progress (bool): Indicates if the game is still in progress.
    """
    
    def __init__(self, root, home_screen):
        """
        Initializes the TicTacToeOnlineUI class, setting up the initial UI 
        and configuring server communication.

        Args:
            root (tk.Tk): The main application window.
            home_screen (HomeScreen): Reference to the home screen for navigating back.
        """
        super().__init__(root, home_screen)
        self.client = None  # Client socket initialized to None
        self.player = None  # Will hold player identifier ('X' or 'O')
        self.turn = False  # Indicates whether it's the player's turn
        self.game_in_progress = True  # Indicates whether the game is ongoing
        self.create_common_controls()  # Set up UI controls

    def create_common_controls(self):
        """
        Calls the base class method to create common controls like the reset button 
        and adds buttons for connecting and disconnecting from the server.
        """
        super().create_common_controls()
        self.create_connect_button()

    def create_connect_button(self):
        """
        Creates and packs the Connect and Disconnect buttons to allow the player 
        to connect and disconnect from the server.
        """
        connect_button = tk.Button(self.root, text="Connect", font=("tahoma", 16), command=self.connect_to_server, fg="white", bg="gray")
        connect_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        disconnect_button = tk.Button(self.root, text="Disconnect", font=("tahoma", 16), command=self.disconnect_from_server, fg="white", bg="gray")
        disconnect_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

    def connect_to_server(self):
        """
        Establishes a connection to the server and receives the player identifier ('X' or 'O'). 
        Starts a separate thread to listen for incoming messages from the server.
        """
        if self.client is not None and self.client.fileno() != -1:
            print("Already connected")
            return
        
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket
            self.client.connect(ADDR)  # Connect to the server at ADDR
            msg_length = self.client.recv(HEADER).decode(FORMAT)  # Receive the length of the incoming message
            if msg_length:
                msg_length = int(msg_length)
                self.player = self.client.recv(msg_length).decode(FORMAT)  # Receive player identifier ('X' or 'O')
                print(f"Connection Successful: Connected as player {self.player}")
                if self.player == 'X':
                    self.turn = True  # Player 'X' always starts first
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)  # Start a thread for receiving messages
            receive_thread.start()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def disconnect_from_server(self):
        """
        Sends a disconnection message to the server and closes the client socket. 
        Also navigates back to the home screen.
        """
        if self.client is None or self.client.fileno() == -1:
            print("No active connection to disconnect.")
            return

        try:
            msg = DISCONNECT_MESSAGE  # Send the disconnection message
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))  # Prepare the message header
            self.client.send(send_length)
            self.client.send(message)
            self.client.close()  # Close the socket connection
            self.client = None
            print("Disconnected from server.")
            self.go_back_home()  # Navigate back to the home screen
        except Exception as e:
            print(f"Error during disconnection: {e}")

    def player_move(self, idx):
        """
        Sends the player's move to the server if it's their turn and the game is still in progress.

        Args:
            idx (int): The index of the cell where the player wants to place their mark.
        """
        if self.turn and self.game_in_progress:
            row, col = idx // 3, idx % 3  # Convert index to row and column
            self.send_coordinate(row, col)

    def send_coordinate(self, row, col):
        """
        Sends the player's move (row and column) to the server in the format "player:row:col".

        Args:
            row (int): The row of the move.
            col (int): The column of the move.
        """
        if not self.turn or not self.game_in_progress:  # Ensure it's the player's turn and the game is ongoing
            print("Not your turn or game over!")
            return
        msg = f"{self.player}:{row}:{col}"  # Format the message to send
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))  # Prepare the message header
        self.client.send(send_length)
        self.client.send(message)
        self.turn = False  # End the player's turn after sending the move

    def receive_messages(self):
        """
        Listens for incoming messages from the server in a separate thread and 
        updates the UI based on the received message.
        """
        while True:
            try:
                msg_length = self.client.recv(HEADER).decode(FORMAT)  # Receive the message length
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.client.recv(msg_length).decode(FORMAT)  # Receive the message content
                    print(f"Received from server: {msg}")

                    if msg.startswith("MOVE"):
                        # Handle incoming move (player, row, col)
                        _, p, row, col = msg.split(':')
                        self.update_board(int(row), int(col), p)  # Update the board with the move
                        if p != self.player:  # If it's the opponent's move, switch the turn to the player
                            self.turn = True
                    elif msg.startswith("WINNER"):
                        # Handle game-winning scenario
                        _, winner = msg.split(':')
                        print(f"{winner} wins!")
                        self.game_over(f"Player {winner} wins!")  # Display the winner message
                    elif msg == "DRAW":
                        # Handle game-draw scenario
                        print("It's a draw!")
                        self.game_over("It's a draw!")  # Display the draw message
                    elif msg == "RESET_BOARD":
                        # Handle board reset
                        self.reset_board()  # Reset the game board
                    elif msg == GAME_OVER_MESSAGE:
                        # Handle game over message
                        print("Game over, returning to home.")
                        self.game_over("Game Over!")  # End the game
                    elif msg == "DISCONNECT":
                        # Handle the scenario where the other player disconnects
                        print("The other player has disconnected. You will be disconnected too.")
                        self.send_disconnect_message()  # Disconnect yourself
                        break  # Break out of the loop
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
