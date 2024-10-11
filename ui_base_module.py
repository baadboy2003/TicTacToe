import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pygame import mixer
from gif_background import GIFLabel  # Import the GIFLabel class

class TicTacToeBaseUI:

    def __init__(self, root, home_screen):
        self.root = root
        self.home_screen = home_screen
        self.buttons = []
        self.button_images = [None] * 9

        # Hide home screen
        self.home_screen.hide_home_screen()

        # Add the GIF background
        gif_label = GIFLabel(self.root, r"background.gif")
        gif_label.pack(fill="both", expand=True)
        gif_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Create the empty image before the board is created
        self.empty_image = ImageTk.PhotoImage(Image.new('RGB', (100, 100), color=(217, 19, 59)))

        # Load and resize images
        self.x_image = Image.open("Cross_m.png").resize((100, 100), resample=Image.BICUBIC)
        self.o_image = Image.open("Circle_m.png").resize((100, 100), resample=Image.BICUBIC)

        # Convert images to PhotoImage
        self.x_photo = ImageTk.PhotoImage(self.x_image)
        self.o_photo = ImageTk.PhotoImage(self.o_image)

        # Initialize win counters
        self.x_wins = 0
        self.o_wins = 0
        self.game_count = 0

        # Create the board after all images are loaded
        self.create_board()


    def create_board(self):
        print("GAME BOARD CREATED!")
        button_size = (100, 100)  # Define a fixed button size

        # Create a frame to center the board
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(expand=True)

        for i in range(9):
            button = tk.Button(self.board_frame, text=" ", font=("Arial", 24), width=button_size[0], height=button_size[1],
                               command=lambda i=i: self.player_move(i), fg="red", bg="silver")
            button.grid(row=i // 3, column=i % 3, sticky="nsew")  # Add sticky="nsew" to make the button expand

            # Set the initial image to the empty image
            button.config(image=self.empty_image)
            self.button_images[i] = None  # Ensure no image is associated with the button yet

            self.buttons.append(button)

        # Configure the rows and columns to have a minimum size
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, minsize=button_size[1], weight=1)  # Set a minimum row size
            self.board_frame.grid_columnconfigure(i, minsize=button_size[0], weight=1)  # Set a minimum column size


    def update_board(self, game_board):
        print("Game Board: ", game_board)
        for i, button in enumerate(self.buttons):
            if game_board[i] == 'X':
                button.config(image=self.x_photo)
            elif game_board[i] == 'O':
                button.config(image=self.o_photo)
            else:
                button.config(image=self.empty_image)


    def reset_board(self):
        for button in self.buttons:
            button.config(image=self.empty_image, state='normal')


    def create_common_controls(self):

        back_button = tk.Button(self.root, text="Back to Home", font=("tahoma", 16), command=self.go_back_home, fg="white", bg="#34cc4c")
        back_button.pack(side=tk.RIGHT, expand=True, padx=10, pady=10)  # Center button with padding
    

    def go_back_home(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.home_screen.create_home_screen()
