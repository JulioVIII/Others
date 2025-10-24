# Math-game #To run this code properly, a text file named winner.txt must exist in the same folder as your script.Without it, the program may fail or throw a FileNotFoundError. 📝
# 🔥 You have 30 seconds to answer as many math problems as possible! 🧮💥
import random
import time
import os

WINNER_FILE = "winner.txt"

def generate_operation():
    """Generates a random math operation."""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(["+", "-", "*"])

    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    else:
        result = num1 * num2

    return f"{num1} {operation} {num2}", result

def read_winner():
    """Reads the highest score safely."""
    if not os.path.exists(WINNER_FILE):
        return ("Nobody", 0)
    with open(WINNER_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return ("Nobody", 0)
        try:
            name, score = content.split(",")
            return name.strip(), int(score.strip())
        except ValueError:
            return ("Nobody", 0)

def save_winner(name, score):
    """Saves a new high score."""
    with open(WINNER_FILE, "w") as f:
        f.write(f"{name},{score}")

def play_game():
    print("🎯 Welcome to the Math Game with Time and High Score!")
    print("You have 30 seconds to answer as many math problems as possible.")
    print("Type 'exit' to quit anytime.\n")

    score = 0
    rounds = 0
    TIME_LIMIT = 30  # seconds
    start_time = time.time()

    player_name = input("Enter your name: ")

    # Read current high score
    current_winner, high_score = read_winner()
    print(f"🏆 Current high score: {high_score} by {current_winner}\n")

    while True:
        time_left = TIME_LIMIT - (time.time() - start_time)
        if time_left <= 0:
            print("\n⏰ Time's up!")
            break

        operation, result = generate_operation()
        rounds += 1

        print(f"Time remaining: {time_left:.1f} seconds")
        answer = input(f"Round {rounds} → What is {operation}? ")

        if answer.lower() == "exit":
            break

        if not answer.strip().lstrip("-").isdigit():
            print("⚠️ Please enter a valid number.\n")
            continue

        if int(answer) == result:
            score += 1
            print("✅ Correct!\n")
        else:
            print(f"❌ Incorrect. The correct answer was {result}.\n")

    print("\n🎮 Game over.")
    print(f"Rounds played: {rounds}")
    print(f"Final score: {score}")
    print(f"Total time played: {time.time() - start_time:.1f} seconds")

    # Check for new high score
    if score > high_score:
        print(f"🎉 Congratulations {player_name}! New world record: {score} points")
        save_winner(player_name, score)
    else:
        print(f"The high score remains {high_score} by {current_winner}")

if __name__ == "__main__":
    play_game()
