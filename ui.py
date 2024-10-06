import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pygame import mixer
from gif_label import GIFLabel  # Import the GIFLabel class

class TicTacToeUI:
    def __init__(self, root, game, home_screen):
        self.root = root
        self.game = game
        self.home_screen = home_screen
        self.buttons = []
        self.button_images = [None] * 9

        # Hide home screen
        self.home_screen.hide_home_screen()

        # Add the GIF background
        gif_label = GIFLabel(self.root, r"arcadegiflol.gif")
        gif_label.pack(fill="both", expand=True)
        gif_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Create a frame to center the board
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(expand=True)

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
        self.create_controls()


    def update_board(self):
        print(self.game.board)
        for i, button in enumerate(self.buttons):
            if self.game.board[i] == 'X':
                if self.button_images[i] is None:
                    button.image = self.x_photo
                    self.button_images[i] = self.x_photo  # Store the image reference
                button.config(image=self.x_photo)
            elif self.game.board[i] == 'O':
                if self.button_images[i] is None:
                    button.image = self.o_photo
                    self.button_images[i] = self.o_photo  # Store the image reference
                button.config(image=self.o_photo)
            else:
                button.config(image=self.empty_image)  # Use the empty image when the space is empty
                self.button_images[i] = None

    def player_move(self, idx):
        mixer.init()
        sound2 = r'ButtonPlate Click (Minecraft Sound) - Sound Effect for editing.mp3'
        sound2_channel = mixer.Channel(1)  # Create a new channel for the second sound
        sound2_channel.play(mixer.Sound(sound2))

        if self.game.game_over:  # Check if the game is over
            return

        if self.game.make_move(idx):
            self.update_board()
            print("1")
            if self.game.check_winner(self.game.current_player):
                if self.game.current_player == "X":
                    self.x_wins += 1
                else:
                    self.o_wins += 1
                self.game_count += 1
                messagebox.showinfo("Tic-Tac-Toe", f"{self.game.current_player} wins this game!")
                self.reset_board()  # Reset the board after showing the messagebox
                self.check_winner()
            elif self.game.board_full():
                self.game_count += 1
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.reset_board()  # Reset the board after showing the messagebox
                self.check_winner()
            else:
                self.game.switch_player()
                print("1 33")
                if self.game.ai_enabled and self.game.current_player == "O":
                    best_move = self.game.ai_move()
                    if best_move is not None:
                        self.game.make_move(best_move)
                        self.update_board()
                        print("2")
                        if self.game.check_winner("O"):
                            self.o_wins += 1
                            self.game_count += 1
                            messagebox.showinfo("Tic-Tac-Toe", "AI wins this game!")
                            self.reset_board()  # Reset the board after showing the messagebox
                            self.check_winner()
                            return
                        elif self.game.board_full():
                            self.game_count += 1
                            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                            self.reset_board()  # Reset the board after showing the messagebox
                            self.check_winner()
                            return
                    self.game.switch_player()
                    print("1 34")

    def check_winner(self):
        if self.x_wins == 2:
            messagebox.showinfo("Tic-Tac-Toe", "X wins the best 2 out of 3!")
            self.go_back_home()
        elif self.o_wins == 2:
            messagebox.showinfo("Tic-Tac-Toe", "O wins the best 2 out of 3!")
            self.go_back_home()
        elif self.game_count == 3:
            if self.x_wins > self.o_wins:
                messagebox.showinfo("Tic-Tac-Toe", "X wins!")
                self.go_back_home()
            elif self.x_wins < self.o_wins:
                messagebox.showinfo("Tic-Tac-Toe", "O wins!")
                self.go_back_home()
            else:
                messagebox.showinfo("Tic-Tac-Toe", "It is a draw!")
                self.go_back_home()

    def go_back_home(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.home_screen.create_home_screen()

    def create_board(self):
        print("GAME BOARD CREATED!")
        button_size = (100, 100)  # Define a fixed button size

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



    def create_controls(self):
        mixer.init()
        sound2 = r'ButtonPlate Click (Minecraft Sound) - Sound Effect for editing.mp3'
        sound2_channel = mixer.Channel(1)  # Create a new channel for the second sound
        sound2_channel.play(mixer.Sound(sound2))

        restart_button = tk.Button(self.root, text="Restart", font=("tahoma", 16), command=self.restart_game, fg="#0a0911", bg="#e6ea14")
        restart_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)  # Center button with padding

        back_button = tk.Button(self.root, text="Back to Home", font=("tahoma", 16), command=self.go_back_home, fg="white", bg="#34cc4c")
        back_button.pack(side=tk.RIGHT, expand=True, padx=10, pady=10)  # Center button with padding

    def restart_game(self):
        self.game.reset_game()
        self.game.game_over = False  # Reset game_over attribute
        for i, button in enumerate(self.buttons):
            button.config(image=self.empty_image)  # Clear the button's image with the empty image
            self.button_images[i] = None  # Clear the image reference
            button.config(text=" ")
            button.config(state="normal")

    def reset_board(self):
        self.game.reset_game()
        self.update_board()
        for button in self.buttons:
            button.config(state="normal")
