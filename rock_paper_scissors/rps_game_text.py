import random

def get_choices():
    player_choice = input("Enter your choice (rock, paper, scrissors): ")
    options = ["rock", "paper", "scissors"]
    computer_choice = random.choice(options)
    choices = {"player": player_choice, "computer": computer_choice}
    return choices

def check_win(player, computer):
    # print("You chose " + player + " and the computer chose " + computer)
    print(f"You chose {player} and the computer chose {computer}.") # Using f strings
    if player == computer:
        return "It's a tie!"
    elif player == "rock":
        if computer == "scissors":
            return "Rock smashes scissors! You win!"
        else:
            return "Paper covers rock! You lose."
    elif player == "paper":
        if computer == "scissors":
            return "Scissors cuts paper! You lose."
        else:
            return "Paper covers rock! You win!"
    elif player == "scissors":
        if computer == "rock":
            return "Rock smashes scissors! You lose."
        else:
            return "Scissors cuts paper! You win!"

choices = get_choices()
result = check_win(choices["player"], choices["computer"])
print(result)

