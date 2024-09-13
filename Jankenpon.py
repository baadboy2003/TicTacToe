import random

#Define parameters
options = ["rock","paper","scissors"]
max_attempt = 3
p_win = 0
p_lose = 0
p_tie = 0
attempt = 0

#Computer Choice
com_gen = random.choice(options)

#User input
def player():
    while True:
        player_choice = str(input("Choose rock, paper or scissors:"))
        if player_choice not in options:
            print("Please input valid choice!")
        else:
            return player_choice

#Compare result and show results
def compare(player_choice):
    global p_win, p_lose, p_tie
    if player_choice == com_gen:
        p_tie +=1
        return "It's a tie!"
    if player_choice == 'scissors':
        if com_gen == 'rock':
            p_lose += 1
            return "Rock smash scissors! You lose!"
        else:
            p_win += 1
            return 'Scissors cut paper! You Win!'
    if player_choice == 'rock':
        if com_gen == 'paper':
            p_lose += 1
            return "Paper beats rock! You lose!"
        else:
            p_win += 1
            return 'Rock smash scissors! You Win!'
    if player_choice == 'paper':
        if com_gen == 'scissors':
            p_lose += 1
            return "Scissors cut paper! You lose!"
        else:
            p_win += 1
            return 'Paper beats rock! You Win!'

#start game
def game_start():
    global attempt
    while attempt < max_attempt:
        player_choice = player()
        output = compare(player_choice)
        print(f"Computer chooses {com_gen}, You choose {player_choice}")
        print(output)
        attempt += 1

    if p_win > p_lose:
        print(f"Game Finish. You won {p_win} matches, lost {p_lose} and have {p_tie} ties! Well Done Baby! ")
    else:
        print(f"Game Finish. I won more matches than you. My win!")

if __name__ == '__main__':
    game_start()


