import tkinter as tk
from game import TicTacToeGame
from ui import TicTacToeUI
from online_ui import OnlineUI  # Import the new OnlineUI class

class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.create_home_screen()

    def create_home_screen(self):
        self.root.title("Tic-Tac-Toe: Select Mode")
        label = tk.Label(self.root, text="Tic-Tac-Toe", font=("Arial", 24))
        label.pack(pady=20)

        single_button = tk.Button(self.root, text="Single Player", font=("Arial", 18),
                                  command=self.start_single_player)
        single_button.pack(pady=10)

        multi_button = tk.Button(self.root, text="Multiplayer", font=("Arial", 18),
                                 command=self.start_multiplayer)
        multi_button.pack(pady=10)

        # New button for Multiplayer Online
        online_multi_button = tk.Button(self.root, text="Multiplayer Online", font=("Arial", 18),
                                        command=self.start_multiplayer_online)
        online_multi_button.pack(pady=10)

    def start_single_player(self):
        self.clear_screen()
        self.start_game(mode="single")

    def start_multiplayer(self):
        self.clear_screen()
        self.start_game(mode="multi")

    def start_multiplayer_online(self):
        self.clear_screen()
        OnlineUI(self.root, self)  # Create and show the OnlineUI same as ui but for online 

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self, mode):
        if mode == "single":
            game = TicTacToeGame(ai_enabled=True)
        elif mode in ["multi"]:  
            game = TicTacToeGame(ai_enabled=False)

        TicTacToeUI(self.root, game, self)
