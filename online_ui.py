import tkinter as tk
import socket
import threading

PORT = 1000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MESSAGE = "D"
GAME_OVER_MESSAGE = "GAME_OVER"

class OnlineUI:
    def __init__(self, root, home_screen):
        self.root = root
        self.home_screen = home_screen
        self.client = None
        self.player = None
        self.turn = False
        self.game_in_progress = True
        self.buttons = []
        self.create_ui()

    def create_ui(self):
        # Create frames
        self.page1 = tk.Frame(self.root)
        self.page2 = tk.Frame(self.root)
        self.page1.pack(fill="both", expand=True)
        self.page2.pack(fill="both", expand=True)
        
        # Create UI for page1 (Home screen)
        connect_button = tk.Button(self.page1, text="Connect", command=self.connect_button)
        connect_button.pack(padx=20, pady=20)

        back_button = tk.Button(self.page1, text="Back to Home", command=self.go_back_home)
        back_button.pack(padx=20, pady=20)

        # Create UI for page2 (Game board)
        self.create_board()

        disconnect_button = tk.Button(self.page2, text="Disconnect", command=self.send_disconnect_message)
        disconnect_button.grid(row=3, column=1, padx=20, pady=20)

    def create_board(self):
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.page2, text="", width=10, height=5,
                                   command=lambda i=i, j=j: self.send_coordinate(i, j))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def connect_button(self):
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
                print(f"Connected as player {self.player}")
                if self.player == 'X':
                    self.turn = True
            self.show_frame(self.page2)
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_disconnect_message(self):
        if self.client is None or self.client.fileno() == -1:
            print("No active connection to disconnect")
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
            print("Disconnected from server")
            self.go_back_home()
        except Exception as e:
            print(f"Error during disconnection: {e}")

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
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state='normal')
        self.game_in_progress = True
        self.turn = (self.player == 'X')

    def game_over(self, message):
        self.game_in_progress = False
        self.display_winner_message(message)

    def display_winner_message(self, message):
        popup = tk.Toplevel()
        popup.title("Game Over")
        label = tk.Label(popup, text=message, font=("Arial", 14))
        label.pack(side="top", fill="x", pady=10)
        ok_button = tk.Button(popup, text="OK", command=lambda: (popup.destroy(), self.reset_board()))
        ok_button.pack(pady=5)

    def update_board(self, row, col, player_mark):
        self.buttons[row][col].config(text=player_mark, state='disabled')

    def show_frame(self, frame):
        frame.tkraise()

    def go_back_home(self):
        # Destroy all widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Recreate and display the home screen
        self.home_screen.create_home_screen()
        self.show_frame(self.home_screen.page1)
