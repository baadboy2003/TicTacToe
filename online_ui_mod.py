import socket
import threading
import tkinter as tk
from base_ui_mod import TicTacToeBaseUI

PORT = 1000       # port for the server 
SERVER = socket.gethostbyname(socket.gethostname())  # gets the IP of the local machine
ADDR = (SERVER, PORT)  # combines server and port   
FORMAT = 'utf-8'      
HEADER = 64
DISCONNECT_MESSAGE = "D"  # message for disconnection sent to the server 
GAME_OVER_MESSAGE = "GAME_OVER"  # message when the game is over

class TicTacToeOnlineUI(TicTacToeBaseUI):
    def __init__(self, root, home_screen):
        super().__init__(root, home_screen)
        self.client = None
        self.player = None
        self.turn = False
        self.game_in_progress = True
        self.create_common_controls()

    def create_common_controls(self):
        super().create_common_controls()
        self.create_connect_button()

    def create_connect_button(self):
        connect_button = tk.Button(self.root, text="Connect", font=("tahoma", 16), command=self.connect_to_server, fg="white", bg="gray")
        connect_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        disconnect_button = tk.Button(self.root, text="Disconnect", font=("tahoma", 16), command=self.disconnect_from_server, fg="white", bg="gray")
        disconnect_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

    def connect_to_server(self):
        if self.client is not None and self.client.fileno() != -1:
            print("Already connected")
            return
        
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)
            msg_length = self.client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                self.player = self.client.recv(msg_length).decode(FORMAT)
                print(f"Connection Successfull: Connected as player {self.player}")
                if self.player == 'X':
                    self.turn = True
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def disconnect_from_server(self):
        if self.client is None or self.client.fileno() == -1:
            print("No active connection to disconnect.")
            return

        try:
            msg = DISCONNECT_MESSAGE
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
            self.client.close()
            self.client = None
            print("Disconnected from server.")
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
        self.turn = False

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
                            self.turn = True
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
                        print("The other player has disconnected. You will be disconnected too.")
                        self.send_disconnect_message()  # Disconnect yourself
                        break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
