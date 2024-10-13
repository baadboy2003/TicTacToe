import socket
import threading
import tkinter as tk
from tkinter import messagebox  # Importing messagebox for role notifications
from ui_base_module import TicTacToeBaseUI

PORT = 1000  # Port for the server
SERVER = '192.168.1.11'  # Gets the IP of the local machine
ADDR = (SERVER, PORT)  # Combines server and port
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MESSAGE = "D"  # Message for disconnection sent to the server
GAME_OVER_MESSAGE = "GAME_OVER"  # Message when the game is over

class TicTacToeOnlineUI(TicTacToeBaseUI):
    def __init__(self, root, home_screen):
        super().__init__(root, home_screen)
        self.client = None
        self.player = None
        self.turn = False
        self.game_in_progress = True
        
        # Create buttons for connecting and disconnecting
        self.connect_button = None
        self.disconnect_button = None
        
        self.create_common_controls()

    def create_common_controls(self):
        super().create_common_controls()
        self.create_connect_button()

    def create_connect_button(self):
        # Connect button to connect to the server
        self.connect_button = tk.Button(self.root, text="Connect", font=("tahoma", 16), command=self.connect_to_server, fg="white", bg="gray")
        self.connect_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        
        # Disconnect button initially disabled
        self.disconnect_button = tk.Button(self.root, text="Disconnect", font=("tahoma", 16), command=self.disconnect_from_server, fg="white", bg="gray", state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

    def connect_to_server(self):
        if self.client is not None and self.client.fileno() != -1:
            print("Already connected")
            return

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)

            # Receive player type (X or O)
            msg_length = self.client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                self.player = self.client.recv(msg_length).decode(FORMAT)
                
                if self.player == "TOO_MANY_PLAYERS":
                    # If server is full, show a message and return to home
                    print("Server full, returning to home.")
                    messagebox.showerror("Server Full", "The server is full. Please try again later.")
                    self.disconnect_from_server()  # Disconnect and return to home
                    return
                
                print(f"Connection Successful: Connected as player {self.player}")
                
                # Notify the player of their role
                self.show_player_role()

                if self.player == 'X':
                    self.turn = True  # Player X starts first

            # Disable connect button and enable disconnect button after connecting
            self.connect_button.config(state=tk.DISABLED)  # Disable the "Connect" button
            self.disconnect_button.config(state=tk.NORMAL)  # Enable the "Disconnect" button

            # Start a thread to receive messages from the server
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()

        except Exception as e:
            print(f"Error connecting to server: {e}")
            messagebox.showerror("Connection Error", "No server to connect to. Returning to Home Screen.")
            self.go_back_home()

    def show_player_role(self):
        """ Show a message box indicating the player's role. """
        role_message = f"You are connected as Player {self.player}!"
        messagebox.showinfo("Player Role", role_message)

    def disconnect_from_server(self):
        if self.client is None or self.client.fileno() == -1:
            print("No active connection to disconnect.")
            return

        try:
            # Send the disconnect message to the server
            self.client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            self.client.close()
            self.client = None
            print("Disconnected from server.")
            
            # Enable connect button and disable disconnect button after disconnecting
            self.connect_button.config(state=tk.NORMAL)  # Re-enable the "Connect" button
            self.disconnect_button.config(state=tk.DISABLED)  # Disable the "Disconnect" button

            self.go_back_home()
        except Exception as e:
            print(f"Error during disconnection: {e}")

    def player_move(self, idx):
        if self.turn and self.game_in_progress:
            row, col = idx // 3, idx % 3
            self.send_coordinate(row, col)

    def send_coordinate(self, row, col):
        if not self.turn or not self.game_in_progress:
            print("Not your turn or game over!")
            return
        msg = f"{self.player}:{row}:{col}"
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        self.turn = False  # Set turn to false after sending the move

    def receive_messages(self):
        while True:
            try:
                msg_length = self.client.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.client.recv(msg_length).decode(FORMAT)
                    print(f"Received from server: {msg}")

                    if msg.startswith("MOVE"):
                        _, p, row, col = msg.split(':')
                        self.update_board(int(row), int(col), p)
                        if p != self.player:
                            self.turn = True  # Set turn to true for the other player
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
                    elif msg == "DISCONNECT":  # New message for disconnection
                        print("The other player has disconnected. Disconnecting both players.")
                        self.disconnect_from_server()  # Disconnect both players
                        break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def update_board(self, row, col, player):
        """ Update the visual board for the corresponding player move. """
        print(f"Updating board for player {player} at ({row}, {col})")
        if player == 'X':
            self.buttons[row * 3 + col].config(image=self.x_photo)
        elif player == 'O':
            self.buttons[row * 3 + col].config(image=self.o_photo)

    def game_over(self, result):
        """ Handle the game-over state and show the result. """
        print(f"Game over: {result}")
        self.game_in_progress = False  # Set the game to not in progress
        tk.messagebox.showinfo("Game Over", result)  # Show result popup
        self.reset_board()  # Reset the board for a new game

    def reset_board(self):
        """ Reset the board visually for a new game. """
        super().reset_board()  # Call the base method to reset the GUI
        self.game_in_progress = True  # Set the game back to in progress
        self.turn = self.player == 'X'  # If player is 'X', give them the first turn
