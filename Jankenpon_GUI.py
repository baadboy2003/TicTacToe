import tkinter as tk
import random

class ScissorsPaperStone:
#Creating GUI
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Scissors Paper Stone")
        self.window.geometry("600x500")

        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0

        self.choices = ["Scissors", "Paper", "Stone"]

#Display both sides choice when battling
        self.player_choice_label = tk.Label(self.window, text="Player's Choice:")
        self.player_choice_label.pack()
        self.computer_choice_label = tk.Label(self.window, text="Computer's Choice:")
        self.computer_choice_label.pack()

#Display End result(who win,who lose)
        self.result_label = tk.Label(self.window, text="Result:")
        self.result_label.pack()

        self.score_label = tk.Label(self.window, text="Score: Player 0 - Computer 0")
        self.score_label.pack()

#Button for player to choose
        self.scissors_button = tk.Button(self.window, text="Scissors", command=lambda: self.play_round("Scissors"))
        self.scissors_button.pack(side=tk.LEFT)

        self.paper_button = tk.Button(self.window, text="Paper", command=lambda: self.play_round("Paper"))
        self.paper_button.pack(side=tk.LEFT)

        self.stone_button = tk.Button(self.window, text="Stone", command=lambda: self.play_round("Stone"))
        self.stone_button.pack(side=tk.LEFT)

#Retry button after game
        self.retry_button = tk.Button(self.window, text="Retry", command=self.retry_game, state=tk.DISABLED)
        self.retry_button.pack()

#1 round game
    def play_round(self, player_choice):
        computer_choice = random.choice(self.choices)

        self.player_choice_label.config(text=f"Player's Choice: {player_choice}")
        self.computer_choice_label.config(text=f"Computer's Choice: {computer_choice}")

#Outcome plus Score counter
        if player_choice == computer_choice:
            result = "It's a tie!"
        elif (player_choice == "Scissors" and computer_choice == "Paper") or \
             (player_choice == "Paper" and computer_choice == "Stone") or \
             (player_choice == "Stone" and computer_choice == "Scissors"):
            result = "Player wins this round!"
            self.player_score += 1
        else:
            result = "Computer wins this round!"
            self.computer_score += 1

        self.result_label.config(text=result)

        self.rounds_played += 1
        self.score_label.config(text=f"Score: Player {self.player_score} - Computer {self.computer_score}")

#To stop game after 3 rounds
        if self.rounds_played == 3:
            if self.player_score > self.computer_score:
                self.result_label.config(text="Player wins the game!")
            elif self.player_score < self.computer_score:
                self.result_label.config(text="Computer wins the game!")
            else:
                self.result_label.config(text="It's a tie game!")

            self.scissors_button.config(state=tk.DISABLED)
            self.paper_button.config(state=tk.DISABLED)
            self.stone_button.config(state=tk.DISABLED)
            self.retry_button.config(state=tk.NORMAL)


#For retry button to work
    def retry_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0

        self.player_choice_label.config(text="Player's Choice:")
        self.computer_choice_label.config(text="Computer's Choice:")
        self.result_label.config(text="Result:")
        self.score_label.config(text="Score: Player 0 - Computer 0")

        self.scissors_button.config(state=tk.NORMAL)
        self.paper_button.config(state=tk.NORMAL)
        self.stone_button.config(state=tk.NORMAL)
        self.retry_button.config(state=tk.DISABLED)

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    game = ScissorsPaperStone()
    game.run()