from ui_base_module import TicTacToeBaseUI
import tkinter as tk
from tkinter import messagebox

class TicTacToeLocalUI(TicTacToeBaseUI):

    def __init__(self, root, game, home_screen):
        super().__init__(root, home_screen)
        self.game = game
        print(f"Game object initialized: {self.game}")
        
        # Create the score labels for both players
        self.create_score_display()
        
        # Create common controls (like the restart button)
        self.create_common_controls()

    def create_score_display(self):
        """Creates the UI elements to display the scores for X and O."""
        self.score_frame = tk.Frame(self.root, bg="black")  # Frame to hold the score labels
        self.score_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Create labels for X and O wins
        self.x_score_label = tk.Label(self.score_frame, text=f"X Wins: {self.x_wins}", font=("Arial", 16), fg="white", bg="black")
        self.o_score_label = tk.Label(self.score_frame, text=f"O Wins: {self.o_wins}", font=("Arial", 16), fg="white", bg="black")
        
        # Pack the labels into the score frame
        self.x_score_label.pack(side=tk.LEFT, padx=10)
        self.o_score_label.pack(side=tk.RIGHT, padx=10)
        
    def player_move(self, idx):
        if self.game.game_over:  # Check if the game is over
            return

        if self.game.make_move(idx):
            self.update_board(self.game.board)
            
            if self.game.check_winner(self.game.current_player):
                if self.game.current_player == "X":
                    self.x_wins += 1
                else:
                    self.o_wins += 1
                self.game_count += 1
                messagebox.showinfo("Tic-Tac-Toe", f"{self.game.current_player} wins this game!")
                self.update_scores()  # Update the score labels
                self.reset_board()  # Reset the board after showing the messagebox
                self.check_winner()
            elif self.game.board_full():
                self.game_count += 1
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.reset_board()  # Reset the board after showing the messagebox
                self.check_winner()
            else:
                self.game.switch_player()

                # AI move if enabled
                if self.game.ai_enabled and self.game.current_player == "O":
                    best_move = self.game.ai_move()
                    if best_move is not None:
                        self.game.make_move(best_move)
                        self.update_board(self.game.board)
                        if self.game.check_winner("O"):
                            self.o_wins += 1
                            self.game_count += 1
                            messagebox.showinfo("Tic-Tac-Toe", "AI wins this game!")
                            self.update_scores()  # Update the score labels
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

    def update_scores(self):
        """Updates the displayed score labels for X and O."""
        self.x_score_label.config(text=f"X Wins: {self.x_wins}")
        self.o_score_label.config(text=f"O Wins: {self.o_wins}")

    def reset_board(self):
        self.game.reset_game()
        super().reset_board()

    def create_common_controls(self):
        super().create_common_controls()
        restart_button = tk.Button(self.root, text="Restart", font=("tahoma", 16), command=self.reset_board, fg="#0a0911", bg="#e6ea14")
        restart_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

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