import tkinter as tk
import socket
import threading
from PIL import Image, ImageTk

PORT = 1000       # port for the server 
SERVER = socket.gethostbyname(socket.gethostname())  # gets the IP of the local machine
ADDR = (SERVER, PORT)  # combines server and port   
FORMAT = 'utf-8'      
HEADER = 64
DISCONNECT_MESSAGE = "D"  # message for disconnection sent to the server 
GAME_OVER_MESSAGE = "GAME_OVER"  # message when the game is over

class OnlineUI:
    def __init__(self, root, home_screen):
        self.root = root
        self.home_screen = home_screen
        self.client = None
        self.player = None
        self.turn = False
        self.game_in_progress = True
        self.buttons = []
        self.button_images = [None] * 9
        self.create_ui()

        # Load images
        self.empty_image = ImageTk.PhotoImage(Image.new('RGB', (200, 200), color=(192, 192, 192)))
        self.x_image = Image.open(r"C:\Users\zahin\Downloads\INF_grp7\inf_grp7\inf_grp7\Cross_m.png")
        self.o_image = Image.open(r"C:\Users\zahin\Downloads\INF_grp7\inf_grp7\inf_grp7\Circle_m.png")
        self.x_image = self.x_image.resize((175, 165), resample=Image.BICUBIC)
        self.o_image = self.o_image.resize((175, 165), resample=Image.BICUBIC)
        self.x_photo = ImageTk.PhotoImage(self.x_image)
        self.o_photo = ImageTk.PhotoImage(self.o_image)

        # Show the home screen initially
        

    def create_ui(self):
        
        self.page2 = tk.Frame(self.root)
    
        self.page2.pack(fill="both", expand=True)

        # Create UI for page2 (Game board)
        self.create_board()

        # Create control buttons for page2
        self.create_controls()

        # Add Connect button on page2
        self.create_connect_button()

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.page2, text=" ", font=("Arial", 24), width=9, height=6,
                               command=lambda i=i: self.send_coordinate(i // 3, i % 3), fg="red", bg="silver")
            button.grid(row=i // 3, column=i % 3, sticky="nsew")
            self.buttons.append(button)

        # Configure rows and columns to ensure layout matches TicTacToeUI
        for i in range(3):
            self.page2.grid_rowconfigure(i, minsize=150, weight=1)
            self.page2.grid_columnconfigure(i, minsize=150, weight=1)

    def create_controls(self):
        # Create Back to Home button on page2
        back_button = tk.Button(self.page2, text="Back to Home", font=("tahoma", 16), command=self.go_back_home,
                                fg="white", bg="gray")
        back_button.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

        # Create Disconnect button on page2
        disconnect_button = tk.Button(self.page2, text="Disconnect", font=("tahoma", 16), command=self.send_disconnect_message,
                                       fg="white", bg="gray")
        disconnect_button.grid(row=3, column=1, sticky="ew", padx=10, pady=10)

    def create_connect_button(self):
        connect_button = tk.Button(self.page2, text="Connect", font=("tahoma", 16), command=self.connect_button,
                                    fg="white", bg="gray")
        connect_button.grid(row=3, column=2, sticky="ew", padx=10, pady=10)

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
                    elif msg == "DISCONNECT":  # New message for disconnection
                        print("The other player has disconnected. You will be disconnected too.")
                        self.send_disconnect_message()  # Disconnect yourself
                        break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break


    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row * 3 + col].config(image=self.empty_image, state='normal')
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
        if player_mark == 'X':
            self.buttons[row * 3 + col].config(image=self.x_photo, state='disabled')
        elif player_mark == 'O':
            self.buttons[row * 3 + col].config(image=self.o_photo, state='disabled')
        else:
            self.buttons[row * 3 + col].config(image=self.empty_image, state='normal')

    

    def go_back_home(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.home_screen.create_home_screen()
        