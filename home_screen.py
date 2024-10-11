import tkinter as tk
from game import TicTacToeGame
from ui import TicTacToeUI
from online_ui_mod import TicTacToeOnlineUI
from local_ui_mod import TicTacToeLocalUI
from online_ui import OnlineUI
from pygame import mixer
from gif_label import GIFLabel  # Import the GIFLabel class


class HomeScreen:
    def __init__(self, root):
        # Initialize pygame mixer and play background music
        mixer.init()
        background_music = r'RobTop - Geometry Dash Menu Theme.mp3'
        mixer.music.load(background_music)
        mixer.music.play(-1)  # Loop indefinitely

        # Store the root window and setup the home screen
        self.root = root
        self.home_widgets = []  # To store references to home screen widgets
        self.create_home_screen()

        # Set window size and properties
        root.geometry("542x602")  # Width x height
        root.resizable(False, False)

    def create_home_screen(self):
        """Create the home screen with game mode options."""
        self.root.title("Tic-Tac-Toe: Select Mode")

        # Background GIF
        gif_label = GIFLabel(self.root, r"arcadegiflol.gif")
        gif_label.pack(fill="both", expand=True)
        gif_label.place(relx=0, rely=0, relwidth=1, relheight=1)  # Background label behind all widgets
        self.home_widgets.append(gif_label)

        # Title Label
        label = tk.Label(self.root, text="Tic-Tac-Toe", font=("Comic Sans MS", 40, "bold"),
                         fg="white", bg="#2f0064", highlightthickness=2, highlightcolor="#666")
        label.pack(pady=50)
        self.home_widgets.append(label)

        # Single Player Button
        single_button = tk.Button(self.root, text="Single Player", font=("tahoma", 20, "bold"),
                                  command=self.start_single_player, fg="white", bg="#633597")
        single_button.pack(pady=10)
        self.home_widgets.append(single_button)

        # Multiplayer Button
        multi_button = tk.Button(self.root, text="Multiplayer", font=("tahoma", 20, "bold"),
                                 command=self.start_multiplayer, fg="white", bg="#633597")
        multi_button.pack(pady=10)
        self.home_widgets.append(multi_button)

        # Multiplayer Online Button
        online_multi_button = tk.Button(self.root, text="Multiplayer Online", font=("tahoma", 20, "bold"),
                                        command=self.start_multiplayer_online, fg="white", bg="#633597")
        online_multi_button.pack(pady=10)
        self.home_widgets.append(online_multi_button)

    def hide_home_screen(self):
        for widget in self.home_widgets:
            widget.pack_forget()  # Hide the home screen widgets

    def start_single_player(self):
        """Start Single Player mode."""
        self.clear_screen()  # Clear home screen widgets
        self.start_game(mode="single")

    def start_multiplayer(self):
        """Start Multiplayer mode."""
        self.clear_screen()  # Clear home screen widgets
        self.start_game(mode="multi")

    def start_multiplayer_online(self):
        """Start Multiplayer Online mode."""
        self.clear_screen()  # Clear home screen widgets
        TicTacToeOnlineUI(self.root, self)  # Switch to online multiplayer UI

    def clear_screen(self):
        """Clear the current screen by destroying all widgets."""
        for widget in self.home_widgets:
            widget.pack_forget()  # You can use pack_forget() if you may need widgets later
        self.home_widgets.clear()  # Clear the list

    def start_game(self, mode):
        """Start the game with the given mode."""
        if mode == "single":
            game = TicTacToeGame(ai_enabled=True)
        elif mode == "multi":
            game = TicTacToeGame(ai_enabled=False)

        # Switch to the game UI
        TicTacToeLocalUI(self.root, game, self)