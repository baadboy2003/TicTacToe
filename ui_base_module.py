import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pygame import mixer
from gif_background import GIFLabel  # Import the GIFLabel class for GIF background support

class TicTacToeBaseUI:
    """
    This class defines the base UI for a Tic-Tac-Toe game using the Tkinter framework. It handles
    the creation of the game board, button controls, and background graphics.

    Attributes:
        root (tk.Tk): The main application window.
        home_screen (HomeScreen): Reference to the home screen object to handle transitions.
        buttons (list): List of button widgets for the game board.
        button_images (list): List to track images assigned to buttons.
        empty_image (ImageTk.PhotoImage): Placeholder image for an empty board cell.
        x_image (Image.Image): Image for player X's marker.
        o_image (Image.Image): Image for player O's marker.
        x_photo (ImageTk.PhotoImage): Resized PhotoImage for player X's marker.
        o_photo (ImageTk.PhotoImage): Resized PhotoImage for player O's marker.
        x_wins (int): Counter for player X's wins.
        o_wins (int): Counter for player O's wins.
        game_count (int): Counter for total number of games played.
    """

    def __init__(self, root, home_screen):
        """
        Initializes the Tic-Tac-Toe UI, hides the home screen, and sets up the game board 
        with images and buttons.

        Args:
            root (tk.Tk): The main application window.
            home_screen (HomeScreen): Reference to the home screen for navigation.
        """
        self.root = root
        self.home_screen = home_screen
        self.buttons = []
        self.button_images = [None] * 9  # Initialize button image list for 9 cells

        # Hide home screen
        self.home_screen.hide_home_screen()

        # Add the GIF background using the custom GIFLabel widget
        gif_label = GIFLabel(self.root, r"./assets/background.gif")
        gif_label.pack(fill="both", expand=True)
        gif_label.place(relx=0, rely=0, relwidth=1, relheight=1)  # Fill the entire window with the GIF

        # Create the empty placeholder image to use before markers are placed on the board
        self.empty_image = ImageTk.PhotoImage(Image.new('RGB', (100, 100), color=(217, 19, 59)))  # Red placeholder

        # Load, resize, and prepare images for X and O markers
        self.x_image = Image.open("./assets/Cross_m.png").resize((100, 100), resample=Image.BICUBIC)
        self.o_image = Image.open("./assets/Circle_m.png").resize((100, 100), resample=Image.BICUBIC)
        self.x_photo = ImageTk.PhotoImage(self.x_image)
        self.o_photo = ImageTk.PhotoImage(self.o_image)

        # Initialize win counters for players
        self.x_wins = 0
        self.o_wins = 0
        self.game_count = 0

        # Create the Tic-Tac-Toe board
        self.create_board()

    def create_board(self):
        """
        Creates the 3x3 Tic-Tac-Toe game board using buttons. Each button represents 
        a cell on the board and triggers a player's move when clicked.
        """
        print("GAME BOARD CREATED!")
        button_size = (100, 100)  # Define a fixed button size for consistency

        # Create a frame to center the game board within the window
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(expand=True)

        # Create 9 buttons for the board (3x3 grid)
        for i in range(9):
            button = tk.Button(self.board_frame, text=" ", font=("Arial", 24), width=button_size[0], height=button_size[1],
                               command=lambda i=i: self.player_move(i), fg="red", bg="silver")
            button.grid(row=i // 3, column=i % 3, sticky="nsew")  # Add sticky="nsew" to ensure the button expands within the cell

            # Set the initial image for each button to the empty placeholder image
            button.config(image=self.empty_image)
            self.button_images[i] = None  # Ensure no image is associated with the button at start

            # Store the button in the buttons list
            self.buttons.append(button)

        # Configure the grid layout for the board, ensuring all rows and columns are equally sized
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, minsize=button_size[1], weight=1)  # Set minimum row height
            self.board_frame.grid_columnconfigure(i, minsize=button_size[0], weight=1)  # Set minimum column width

    def update_board(self, game_board):
        """
        Updates the game board UI based on the current game state by assigning 'X' and 'O' images 
        to the corresponding buttons.

        Args:
            game_board (list): List representing the current game state, with 'X', 'O', or empty spaces.
        """
        print("Game Board: ", game_board)
        for i, button in enumerate(self.buttons):
            if game_board[i] == 'X':
                button.config(image=self.x_photo)  # Set the 'X' marker image
            elif game_board[i] == 'O':
                button.config(image=self.o_photo)  # Set the 'O' marker image
            else:
                button.config(image=self.empty_image)  # Set the empty placeholder image

    def reset_board(self):
        """
        Resets the game board for a new game, clearing all markers and enabling all buttons.
        """
        for button in self.buttons:
            button.config(image=self.empty_image, state='normal')  # Reset button images and enable all buttons

    def create_common_controls(self):
        """
        Creates common controls such as the 'Back to Home' button, which allows the player 
        to navigate back to the home screen.
        """
        # Create and pack a 'Back to Home' button
        back_button = tk.Button(self.root, text="Back to Home", font=("tahoma", 16), command=self.go_back_home, fg="white", bg="#34cc4c")
        back_button.pack(side=tk.RIGHT, expand=True, padx=10, pady=10)  # Place the button on the right side with padding

    def go_back_home(self):
        """
        Handles navigation back to the home screen by destroying all current widgets
        and re-initializing the home screen.
        """
        # Destroy all widgets in the current window
        for widget in self.root.winfo_children():
            widget.destroy()
        # Recreate the home screen
        self.home_screen.create_home_screen()
