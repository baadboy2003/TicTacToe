import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk

def computer_options():
    return ["Rock", "Paper", "Scissor"]

#Compare result and outcomes
def game(player):
    computer = random.choice(computer_options())
    if player == computer:
        return "Match Draw"
    if (player == "Rock" and computer == "Scissor") or (player == "Scissor" and computer == "Paper") or (player == "Paper" and computer == "Rock"):
        return "Player Win"
    else:
        return "Computer Win"

# creating GUI
class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("600x600")

        self.player_score = 0
        self.computer_score = 0

        self.player_score_label = ttk.Label(root, text="Player Score: 0")
        self.player_score_label.pack()

        self.computer_score_label = ttk.Label(root, text="Computer Score: 0")
        self.computer_score_label.pack()

        self.result_label = ttk.Label(root, text="")
        self.result_label.pack()

        # Load images
        rock_image = Image.open("rock.png")
        paper_image = Image.open("paper.png")
        scissor_image = Image.open("scissors.png")

        # Resize images
        rock_image = rock_image.resize((190, 190) )
        paper_image = paper_image.resize((190, 190))
        scissor_image = scissor_image.resize((190, 190))

        # Convert images to PhotoImage
        rock_photo = ImageTk.PhotoImage(rock_image)
        paper_photo = ImageTk.PhotoImage(paper_image)
        scissor_photo = ImageTk.PhotoImage(scissor_image)

        # Create buttons with images
        self.rock_button = ttk.Button(root, image=rock_photo, command=lambda: self.play("Rock"))
        self.rock_button.image = rock_photo
        self.rock_button.pack(side=tk.LEFT)

        self.paper_button = ttk.Button(root, image=paper_photo, command=lambda: self.play("Paper"))
        self.paper_button.image = paper_photo
        self.paper_button.pack(side=tk.LEFT)

        self.scissor_button = ttk.Button(root, image=scissor_photo, command=lambda: self.play("Scissor"))
        self.scissor_button.image = scissor_photo
        self.scissor_button.pack(side=tk.RIGHT)

    def play(self, player):
        computer = random.choice(computer_options())
        result = game(player)
        if result == "Player Win":
            self.player_score += 1
        elif result == "Computer Win":
            self.computer_score += 1
        self.player_score_label['text'] = f"Player Score: {self.player_score}"
        self.computer_score_label['text'] = f"Computer Score: {self.computer_score}"
        self.result_label['text'] = f"Computer chose {computer}. {result}"

root = tk.Tk()
my_game = RockPaperScissors(root)
root.mainloop()