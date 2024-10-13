import tkinter as tk
from game_logic import TicTacToeGame
from ui_online_module import TicTacToeOnlineUI
from ui_local_module import TicTacToeLocalUI
from pygame import mixer
from gif_background import GIFLabel  # Import the GIFLabel class for GIF background support

class HomeScreen:
    """
    This class defines the home screen for the Tic-Tac-Toe game. It provides options 
    for selecting the game mode (Single Player, Multiplayer, or Multiplayer Online) 
    and initializes the necessary game settings.
    
    Attributes:
        root (tk.Tk): The main application window.
        home_widgets (list): List of widgets used on the home screen, to manage visibility.
    """

    def __init__(self, root):
        """
        Initializes the home screen, sets up background music, and creates the mode 
        selection screen with buttons.

        Args:
            root (tk.Tk): The main application window.
        """
        # Initialize pygame mixer and play background music
        mixer.init()
        background_music = r'RobTop - Geometry Dash Menu Theme.mp3'
        mixer.music.load(background_music)
        mixer.music.play(-1)  # Loop indefinitely

        # Store the root window and setup the home screen widgets
        self.root = root
        self.home_widgets = []  # To store references to home screen widgets for later manipulation
        self.create_home_screen()

        # Set window size and properties (fixed size, non-resizable)
        root.geometry("542x602")  # Width x height
        root.resizable(False, False)

    def create_home_screen(self):
        """
        Create the home screen UI with options to select game modes (Single Player, 
        Multiplayer, and Multiplayer Online).
        """
        self.root.title("Tic-Tac-Toe: Select Mode")

        # Add the background GIF using the custom GIFLabel widget
        gif_label = GIFLabel(self.root, r"background.gif")
        gif_label.pack(fill="both", expand=True)
        gif_label.place(relx=0, rely=0, relwidth=1, relheight=1)  # Set the GIF as the background
        self.home_widgets.append(gif_label)  # Store widget reference

        # Title Label
        label = tk.Label(self.root, text="Tic-Tac-Toe", font=("Comic Sans MS", 40, "bold"),
                         fg="white", bg="#2f0064", highlightthickness=2, highlightcolor="#666")
        label.pack(pady=50)  # Add padding to position title properly
        self.home_widgets.append(label)  # Store widget reference

        # Single Player Button
        single_button = tk.Button(self.root, text="Single Player", font=("tahoma", 20, "bold"),
                                  command=self.start_single_player, fg="white", bg="#633597")
        single_button.pack(pady=10)  # Padding between buttons
        self.home_widgets.append(single_button)  # Store widget reference

        # Multiplayer Button
        multi_button = tk.Button(self.root, text="Multiplayer", font=("tahoma", 20, "bold"),
                                 command=self.start_multiplayer, fg="white", bg="#633597")
        multi_button.pack(pady=10)  # Padding between buttons
        self.home_widgets.append(multi_button)  # Store widget reference

        # Multiplayer Online Button
        online_multi_button = tk.Button(self.root, text="Multiplayer Online", font=("tahoma", 20, "bold"),
                                        command=self.start_multiplayer_online, fg="white", bg="#633597")
        online_multi_button.pack(pady=10)  # Padding between buttons
        self.home_widgets.append(online_multi_button)  # Store widget reference

    def hide_home_screen(self):
        """
        Hide the home screen widgets, making them invisible while the game mode is active.
        """
        for widget in self.home_widgets:
            widget.pack_forget()  # Hide each widget without destroying them

    def start_single_player(self):
        """
        Start Single Player mode by clearing the home screen and initializing the game in 
        single-player mode (with AI enabled).
        """
        self.clear_screen()  # Clear home screen widgets
        self.start_game(mode="single")  # Start the game in single-player mode

    def start_multiplayer(self):
        """
        Start Multiplayer mode by clearing the home screen and initializing the game 
        in multiplayer mode (without AI).
        """
        self.clear_screen()  # Clear home screen widgets
        self.start_game(mode="multi")  # Start the game in multiplayer mode

    def start_multiplayer_online(self):
        """
        Start Multiplayer Online mode by clearing the home screen and switching to 
        the online multiplayer UI.
        """
        self.clear_screen()  # Clear home screen widgets
        TicTacToeOnlineUI(self.root, self)  # Switch to online multiplayer UI

    def clear_screen(self):
        """
        Clear the current screen by hiding all home screen widgets and clearing the 
        widget list.
        """
        for widget in self.home_widgets:
            widget.pack_forget()  # Hide widgets (but do not destroy them)
        self.home_widgets.clear()  # Clear the list of home screen widgets

    def start_game(self, mode):
        """
        Start the game based on the selected mode (single or multiplayer).
        
        Args:
            mode (str): Mode of the game. Can be 'single' (with AI) or 'multi' (without AI).
        """
        if mode == "single":
            game = TicTacToeGame(ai_enabled=True)  # Initialize game with AI for single-player
        elif mode == "multi":
            game = TicTacToeGame(ai_enabled=False)  # Initialize game without AI for multiplayer

        # Switch to the game UI
        TicTacToeLocalUI(self.root, game, self)  # Start the local multiplayer or single-player UI