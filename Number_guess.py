import random
#farhan
#Define parameters
lower_value = 0
upper_value = 0
total_attempts = 10
com_gen = 0

while True:
    Difficulty = str(input("Select difficulty: Easy or Hard:"))
    if Difficulty == "Easy":
        lower_value = 1
        upper_value = 100
        break
    elif Difficulty == "Hard":
        lower_value = 1
        upper_value = 1000
        break
    else:
        print("Invalid please try again!")

#Start game by computer generating number
com_gen = int(random.randint(lower_value, upper_value))

# Get player guess
def player_number():
    while True:
        player_guess = int(input(f"Think of number between {lower_value} and  {upper_value}:"))
        if player_guess >= lower_value or player_guess <= upper_value :
            return player_guess
        else:
            print("Invalid number. Please input number within range")

#compare player's accuracy
def compare_guesses(player_guess, com_gen):
    if player_guess == com_gen:
        return 'Good Job Baby!'
    elif 0 <(com_gen - player_guess) <= 5:
        return "So close!a little higher"
    elif 0 <(player_guess - com_gen) <= 5:
        return "So close! a little smaller"
    elif player_guess < com_gen:
        return 'Too Low! Think higher'
    else:
        return "Too high! think smaller"

# To ensure only 10 attempts then game over
def game_start():
    attempts = 0
    win = False

    while attempts < total_attempts:
        player_guess = player_number()
        output = compare_guesses(player_guess, com_gen)
        attempts +=1

        if output == "Good Job Baby!":
            print(f"Well done! You guessed the number {com_gen} in {attempts} tries.")
            win = True
            break
        else:
            print(f"{output}. Don,t give up! Try again>")

    if not win:
        print(f"Sorry, no more tries! The number is {com_gen}!")

#Player,s View
if __name__ == '__main__':
    print("Welcome to the game, Let's play!")
    game_start()