from ui_base_module import TicTacToeBaseUI
import tkinter as tk
from tkinter import messagebox

class TicTacToeLocalUI(TicTacToeBaseUI):
    """
    The TicTacToeLocalUI class is responsible for handling the local multiplayer UI 
    for the Tic-Tac-Toe game. It extends the TicTacToeBaseUI class and includes 
    score tracking, game controls, and user interactions.

    Attributes:
        game (TicTacToeGame): The game logic for managing Tic-Tac-Toe moves and state.
        home_screen (HomeScreen): Reference to the home screen to allow returning 
                                  to the home screen after finishing the game.
    """

    def __init__(self, root, game, home_screen):
        """
        Initialize the TicTacToeLocalUI, set up the score display, and create common controls.

        Args:
            root (tk.Tk): The main application window.
            game (TicTacToeGame): Instance of the game logic to manage the game state.
            home_screen (HomeScreen): Reference to the home screen for navigating back.
        """
        super().__init__(root, home_screen)
        self.game = game
        print(f"Game object initialized: {self.game}")

        # Create the score display for X and O wins
        self.create_score_display()

        # Create common controls like the restart button
        self.create_common_controls()

    def create_score_display(self):
        """
        Create the UI elements to display the scores for player X and player O.
        """
        self.score_frame = tk.Frame(self.root, bg="black")  # Frame to hold the score labels
        self.score_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Labels for X and O wins, initialized with current scores
        self.x_score_label = tk.Label(self.score_frame, text=f"X Wins: {self.x_wins}", font=("Arial", 16), fg="white", bg="black")
        self.o_score_label = tk.Label(self.score_frame, text=f"O Wins: {self.o_wins}", font=("Arial", 16), fg="white", bg="black")

        # Pack the labels into the score frame (X on the left, O on the right)
        self.x_score_label.pack(side=tk.LEFT, padx=10)
        self.o_score_label.pack(side=tk.RIGHT, padx=10)

    def player_move(self, idx):
        """
        Handle the player's move on the game board.

        Args:
            idx (int): The index of the cell where the player attempts to make a move.
        """
        if self.game.game_over:  # Do nothing if the game is over
            return

        if self.game.make_move(idx):  # Update the game state with the player's move
            self.update_board(self.game.board)  # Refresh the UI board

            if self.game.check_winner(self.game.current_player):  # Check if the current player won
                if self.game.current_player == "X":
                    self.x_wins += 1  # Increment X's win count
                else:
                    self.o_wins += 1  # Increment O's win count
                self.game_count += 1  # Increment game count
                messagebox.showinfo("Tic-Tac-Toe", f"{self.game.current_player} wins this game!")
                self.update_scores()  # Update the displayed scores
                self.reset_board()  # Reset the game board for a new game
                self.check_winner()  # Check if someone won the best 2 out of 3
            elif self.game.board_full():  # Check if the board is full for a draw
                self.game_count += 1
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.reset_board()  # Reset the game board after a draw
                self.check_winner()  # Check if the game series is over
            else:
                self.game.switch_player()  # Switch to the other player

                # If AI is enabled, make the AI's move
                if self.game.ai_enabled and self.game.current_player == "O":
                    best_move = self.game.ai_move()  # Get the AI's best move
                    if best_move is not None:
                        self.game.make_move(best_move)  # Make the AI's move
                        self.update_board(self.game.board)  # Refresh the UI board
                        if self.game.check_winner("O"):  # Check if AI won
                            self.o_wins += 1
                            self.game_count += 1
                            messagebox.showinfo("Tic-Tac-Toe", "AI wins this game!")
                            self.update_scores()  # Update the displayed scores
                            self.reset_board()  # Reset the game board for a new game
                            self.check_winner()  # Check if someone won the best 2 out of 3
                            return
                        elif self.game.board_full():  # Check for a draw after AI's move
                            self.game_count += 1
                            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                            self.reset_board()  # Reset the game board after a draw
                            self.check_winner()
                            return
                    self.game.switch_player()  # Switch back to the player

    def update_scores(self):
        """
        Update the score labels for player X and player O to reflect the current scores.
        """
        self.x_score_label.config(text=f"X Wins: {self.x_wins}")  # Update X's score label
        self.o_score_label.config(text=f"O Wins: {self.o_wins}")  # Update O's score label

    def reset_board(self):
        """
        Reset the game board for a new game.
        """
        self.game.reset_game()  # Reset the game logic
        super().reset_board()  # Reset the UI board

    def create_common_controls(self):
        """
        Create common controls like the restart button.
        """
        super().create_common_controls()  # Call the base class method to set up common controls
        # Create and pack the Restart button
        restart_button = tk.Button(self.root, text="Restart", font=("tahoma", 16), command=self.reset_board, fg="#0a0911", bg="#e6ea14")
        restart_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

    def check_winner(self):
        """
        Check if a player has won the best 2 out of 3 games. Show a message and return to the home screen if the series is complete.
        """
        if self.x_wins == 2:  # If X wins 2 games
            messagebox.showinfo("Tic-Tac-Toe", "X wins the best 2 out of 3!")
            self.go_back_home()  # Return to the home screen
        elif self.o_wins == 2:  # If O wins 2 games
            messagebox.showinfo("Tic-Tac-Toe", "O wins the best 2 out of 3!")
            self.go_back_home()  # Return to the home screen
        elif self.game_count == 3:  # If 3 games have been played
            if self.x_wins > self.o_wins:
                messagebox.showinfo("Tic-Tac-Toe", "X wins!")
                self.go_back_home()  # Return to the home screen
            elif self.x_wins < self.o_wins:
                messagebox.showinfo("Tic-Tac-Toe", "O wins!")
                self.go_back_home()  # Return to the home screen
            else:
                messagebox.showinfo("Tic-Tac-Toe", "It is a draw!")
                self.go_back_home()  # Return to the home screen
