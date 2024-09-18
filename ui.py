import tkinter as tk
from tkinter import messagebox

class TicTacToeUI:
    def __init__(self, root, game, home_screen):
        self.root = root
        self.game = game
        self.home_screen = home_screen
        self.buttons = []
        self.create_board()
        self.create_controls()

    def update_board(self):
        print(self.game.board)
        for i, button in enumerate(self.buttons):
            button.config(text=self.game.board[i])

    def player_move(self, idx):
        if self.game.game_over:  # Check if the game is over
            return

        if self.game.make_move(idx):
            self.update_board()
            print("1")
            if self.game.check_winner(self.game.current_player):
                messagebox.showinfo("Tic-Tac-Toe", f"{self.game.current_player} wins!")
                self.game.game_over = True  # Set game as over
                self.reset_board()  # Reset the board after showing the messagebox
            elif self.game.board_full():
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.game.game_over = True  # Set game as over
                self.reset_board()  # Reset the board after showing the messagebox
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
                            messagebox.showinfo("Tic-Tac-Toe", "AI wins!")
                            self.game.game_over = True  # Set game as over
                            self.restart_game()  # Reset the board after showing the messagebox
                            return
                        elif self.game.board_full():
                            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                            self.game.game_over = True  # Set game as over
                            self.restart_game()  # Reset the board after showing the messagebox
                            return
                    self.game.switch_player()
                    print("1 34")



    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text=" ", font=("Arial", 24), width=5, height=2,
                               command=lambda i=i: self.player_move(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    def create_controls(self):
        restart_button = tk.Button(self.root, text="Restart", font=("Arial", 16),
                                   command=self.restart_game)
        restart_button.grid(row=3, column=0, columnspan=2, sticky="ew")

        back_button = tk.Button(self.root, text="Back to Home", font=("Arial", 16),
                                command=self.go_back_home)
        back_button.grid(row=3, column=2, columnspan=2, sticky="ew")

    def restart_game(self):
        self.game.reset_game()
        self.update_board()
        print("3")

    def go_back_home(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.home_screen.create_home_screen()
    
    def reset_board(self):
        self.game.reset_game()
        self.update_board()
        print("4")

