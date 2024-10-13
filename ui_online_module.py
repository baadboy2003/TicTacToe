import socket
import threading
import tkinter as tk
from tkinter import messagebox  # Importing messagebox for role notifications
from ui_base_module import TicTacToeBaseUI

PORT = 1000  # Port for the server
SERVER = '192.168.1.11'  # Local IP address of the server
ADDR = (SERVER, PORT)  # Combine server and port into an address tuple
FORMAT = 'utf-8'  # Encoding format for communication
HEADER = 64  # Fixed header size for message lengths
DISCONNECT_MESSAGE = "D"  # Message to indicate disconnection to the server
GAME_OVER_MESSAGE = "GAME_OVER"  # Message indicating the game is over

class TicTacToeOnlineUI(TicTacToeBaseUI):
    """
    UI class for handling the online multiplayer mode of Tic-Tac-Toe.
    Inherits from TicTacToeBaseUI for common game UI components.
    Manages connection to the server and player interactions over the network.
    """
    
    def __init__(self, root, home_screen):
        """
        Initialize the TicTacToeOnlineUI class.

        Args:
            root: The main Tkinter window.
            home_screen: Reference to the home screen UI.
        """
        super().__init__(root, home_screen)
        self.client = None  # Socket client for server connection
        self.player = None  # Player type ('X' or 'O')
        self.turn = False  # Keeps track of whether it's the player's turn
        self.game_in_progress = True  # Flag for game state
        
        # Create buttons for connecting and disconnecting
        self.connect_button = None
        self.disconnect_button = None
        
        # Initialize the common UI controls
        self.create_common_controls()

    def create_common_controls(self):
        """ Creates the common UI components and controls for the online mode. """
        super().create_common_controls()  # Call base UI components
        self.create_connect_button()  # Add the connect button

    def create_connect_button(self):
        """ Create the 'Connect' and 'Disconnect' buttons for server connection management. """
        # Button to connect to the server
        self.connect_button = tk.Button(self.root, text="Connect", font=("tahoma", 16), command=self.connect_to_server, fg="white", bg="gray")
        self.connect_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        
        # Button to disconnect from the server, initially disabled
        self.disconnect_button = tk.Button(self.root, text="Disconnect", font=("tahoma", 16), command=self.disconnect_from_server, fg="white", bg="gray", state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

    def connect_to_server(self):
        """ Handles connection to the Tic-Tac-Toe server. Sets up the client socket and manages the initial communication. """
        if self.client is not None and self.client.fileno() != -1:
            print("Already connected")  # If already connected, return
            return

        try:
            # Create a new socket connection to the server
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)  # Connect to the server address

            # Receive the player type (X or O) from the server
            msg_length = self.client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                self.player = self.client.recv(msg_length).decode(FORMAT)
                
                # If server is full, notify the user and return to the home screen
                if self.player == "TOO_MANY_PLAYERS":
                    print("Server full, returning to home.")
                    messagebox.showerror("Server Full", "The server is full. Please try again later.")
                    self.disconnect_from_server()
                    return
                
                print(f"Connection Successful: Connected as player {self.player}")
                
                # Show player's role (X or O)
                self.show_player_role()

                # Player X starts first
                if self.player == 'X':
                    self.turn = True

            # Disable the 'Connect' button and enable the 'Disconnect' button
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)

            # Start a new thread to handle receiving messages from the server
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()

        except Exception as e:
            print(f"Error connecting to server: {e}")
            messagebox.showerror("Connection Error", "No server to connect to. Returning to Home Screen.")
            self.go_back_home()

    def show_player_role(self):
        """ Displays a message box showing whether the player is X or O. """
        role_message = f"You are connected as Player {self.player}!"
        messagebox.showinfo("Player Role", role_message)

    def disconnect_from_server(self):
        """ Handles disconnection from the server. Cleans up the client socket and resets UI controls. """
        if self.client is None or self.client.fileno() == -1:
            print("No active connection to disconnect.")
            return

        try:
            # Send disconnect message to the server
            self.client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            self.client.close()  # Close the socket connection
            self.client = None
            print("Disconnected from server.")
            
            # Reset UI buttons
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)

            # Return to the home screen
            self.go_back_home()
        except Exception as e:
            print(f"Error during disconnection: {e}")

    def player_move(self, idx):
        """ Handles the player's move on the board, sending the move coordinates to the server. """
        if self.turn and self.game_in_progress:
            row, col = idx // 3, idx % 3  # Convert button index to row and column
            self.send_coordinate(row, col)

    def send_coordinate(self, row, col):
        """ Sends the player's move (row and column) to the server. """
        if not self.turn or not self.game_in_progress:
            print("Not your turn or game over!")
            return

        # Prepare message with player's move
        msg = f"{self.player}:{row}:{col}"
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))  # Padding to match HEADER size

        # Send message length and message itself to the server
        self.client.send(send_length)
        self.client.send(message)

        # After sending the move, it's the other player's turn
        self.turn = False

    def receive_messages(self):
        """ Continuously listens for messages from the server, processing game updates or disconnection. """
        while True:
            try:
                # Receive message length and message from the server
                msg_length = self.client.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.client.recv(msg_length).decode(FORMAT)
                    print(f"Received from server: {msg}")

                    # Handle different types of messages
                    if msg.startswith("MOVE"):
                        _, p, row, col = msg.split(':')
                        self.update_board(int(row), int(col), p)
                        if p != self.player:
                            self.turn = True  # Set turn for the other player
                    elif msg.startswith("WINNER"):
                        _, winner = msg.split(':')
                        print(f"{winner} wins!")
                        self.game_over(f"Player {winner} wins!")
                    elif msg == "DRAW":
                        print("It's a draw!")
                        self.game_over("It's a draw!")
                    elif msg == "RESET_BOARD":
                        self.reset_board()
                    elif msg == GAME_OVER_MESSAGE:
                        print("Game over, returning to home.")
                        self.game_over("Game Over!")
                    elif msg == "DISCONNECT":
                        print("The other player has disconnected. Disconnecting both players.")
                        self.disconnect_from_server()  # Disconnect if other player leaves
                        break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def update_board(self, row, col, player):
        """ Updates the game board to reflect the player's move. """
        print(f"Updating board for player {player} at ({row}, {col})")
        if player == 'X':
            self.buttons[row * 3 + col].config(image=self.x_photo)  # Update button to X
        elif player == 'O':
            self.buttons[row * 3 + col].config(image=self.o_photo)  # Update button to O

    def game_over(self, result):
        """ Ends the game, showing a result message and resetting the board. """
        print(f"Game over: {result}")
        self.game_in_progress = False  # Set game as no longer in progress
        tk.messagebox.showinfo("Game Over", result)  # Show game-over message
        self.reset_board()  # Reset the board for a new game

    def reset_board(self):
        """ Resets the visual game board for a new game. """
        super().reset_board()  # Call base class method to reset the board
        self.game_in_progress = True  # Set game as in progress
        self.turn = self.player == 'X'  # If player is 'X', they start first
