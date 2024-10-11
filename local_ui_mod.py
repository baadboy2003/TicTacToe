from base_ui_mod import TicTacToeBaseUI
import tkinter as tk
from tkinter import messagebox

class TicTacToeLocalUI(TicTacToeBaseUI):

    def __init__(self, root, game, home_screen):
        super().__init__(root, home_screen)
        self.game = game
        print(f"Game object initialized: {self.game}")
        self.create_common_controls()

    def player_move(self, idx):


        if self.game.game_over:  # Check if the game is over
            return

        if self.game.make_move(idx):
            self.update_board(self.game.board)
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
                        self.update_board(self.game.board)
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

    def reset_board(self):
        self.game.reset_game()
        super().reset_board()

    def create_common_controls(self):
        print(f"restart button: {self}")
        super().create_common_controls()
        restart_button = tk.Button(self.root, text="Restart", font=("tahoma", 16), command=self.reset_board, fg="#0a0911", bg="#e6ea14")
        restart_button.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
