import random
import os.path
import json

random.seed()

last_player_name = ""
last_score = None


def draw_board(board):
    """Print the current state of the noughts and crosses board.

    The board is a 3x3 list of lists containing "X", "O" or " ".
    This function only displays the board; it does not modify it.
    """
    for row_index, row in enumerate(board):
        print(" | ".join(row))
        if row_index < 2:
            print("--+---+--")


def welcome(board):
    """Print a welcome message and display the starting board."""
    print('Welcome to "Unbeatable Noughts and Crosses"  @Made by Sudarshan Mishra')
    print("The board positions are as follows:")
    draw_board(board)
    print("You are X and you go first.")


def initialise_board(board):
    """Set all elements of the board to a single space ' ' and return it."""
    for i in range(3):
        for j in range(3):
            board[i][j] = " "
    return board


def get_player_details():
    """Ask for player details (name) before starting a game and store it."""
    while True:
        name = input("Please enter your name: ").strip()
        if name:
            global last_player_name
            last_player_name = name
            print(f"Hello, {name}.")
            return name
        print("Name cannot be empty. Please try again.")


def get_player_move(board):
    """Ask the user for the cell to put the X in and return row and col."""
    while True:
        choice = input("Enter a number between 1 and 9 to place your X: ")
        if not choice.isdigit():
            print("Invalid input. Please enter a number between 1 and 9.")
            continue

        num = int(choice)
        if num < 1 or num > 9:
            print("Number out of range. Please choose between 1 and 9.")
            continue

        row = (num - 1) // 3
        col = (num - 1) % 3

        if board[row][col] != " ":
            print("That square is already taken. Choose another one.")
            continue

        return row, col


def choose_computer_move(board):
    """Choose a move for the computer (O) and return row and col.

    First, try every empty square by placing an O there temporarily
    to see if it results in a win. If a winning move is found, use it.
    Otherwise, choose a random empty square.
    """
    # Try to find a winning move
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                if check_for_win(board, "O"):
                    board[i][j] = " "  # reset after testing
                    return i, j
                board[i][j] = " "  # reset if not winning

    # No winning move found, choose a random empty square
    empty_squares = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                empty_squares.append((i, j))

    if not empty_squares:
        # Should not happen if called correctly, but safe guard
        return 0, 0

    return random.choice(empty_squares)


def check_for_win(board, mark):
    """Check if the player with the given mark has won.

    Returns True if there are three of the given mark in a row,
    column or diagonal, otherwise False.
    """
    # Check rows
    for i in range(3):
        if board[i][0] == mark and board[i][1] == mark and board[i][2] == mark:
            return True

    # Check columns
    for j in range(3):
        if board[0][j] == mark and board[1][j] == mark and board[2][j] == mark:
            return True

    # Check diagonals
    if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
        return True
    if board[0][2] == mark and board[1][1] == mark and board[2][0] == mark:
        return True

    return False


def check_for_draw(board):
    """Return True if all cells are occupied, otherwise False."""
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return False
    return True


def play_game(board):
    """Play one full game and return the score.

    Score:
    1  - player (X) wins
    -1 - computer (O) wins
    0  - draw
    """
    initialise_board(board)
    print("Starting a new game.")
    draw_board(board)

    while True:
        # Player move
        row, col = get_player_move(board)
        board[row][col] = "X"
        draw_board(board)

        if check_for_win(board, "X"):
            print("Congratulations, you win!")
            return 1

        if check_for_draw(board):
            print("The game is a draw.")
            return 0

        # Computer move
        print("Computer is making a move...")
        row, col = choose_computer_move(board)
        board[row][col] = "O"
        draw_board(board)

        if check_for_win(board, "O"):
            print("The computer wins.")
            return -1

        if check_for_draw(board):
            print("The game is a draw.")
            return 0


def menu():
    """Display the menu and get user input of '1', '2', '3' or 'q'."""
    while True:
        print()
        print("Menu:")
        print("1 - Play the game")
        print("2 - Save score in file 'leaderboard.txt'")
        print("3 - Load and display the scores from 'leaderboard.txt'")
        print("q - End the program")
        choice = input("Enter your choice: ").strip()
        if choice in ("1", "2", "3", "q"):
            return choice
        print("Invalid choice, please try again.")


def load_scores():
    """Load the leaderboard scores from 'leaderboard.txt'.

    Returns a dictionary with player names as keys and scores as values.
    If the file does not exist or is empty, an empty dictionary is returned.
    """
    leaders = {}
    filename = "leaderboard.txt"

    if not os.path.isfile(filename):
        return leaders

    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if content:
                leaders = json.loads(content)
    except (OSError, json.JSONDecodeError):
        # If there is any problem reading/parsing, return empty dict
        leaders = {}

    return leaders
    

def save_score(score):
    """Ask the player for their name and save the score to 'leaderboard.txt'."""
    name = last_player_name if last_player_name else input("Please enter your name: ").strip()
    if not name:
        print("Name cannot be empty. Score not saved.")
        return

    leaders = load_scores()
    leaders[name] = score

    try:
        with open("leaderboard.txt", "w", encoding="utf-8") as file:
            file.write(json.dumps(leaders))
        print("Score saved successfully.")
    except OSError:
        print("An error occurred while saving the score.")


def display_leaderboard(leaders):
    """Display the leaderboard scores from the leaders dictionary."""
    if not leaders:
        print("No scores to display.")
        return

    print("Leaderboard:")
    for name, score in leaders.items():
        print(f"{name}: {score}")
        
        
if __name__ == "__main__":
    board = [[" " for _ in range(3)] for _ in range(3)]
    welcome(board)
    while True:
        choice = menu()
        if choice == "1":
            get_player_details()
            last_score = play_game(board)
        elif choice == "2":
            if last_score is None:
                print("No score available. Play a game first.")
            else:
                save_score(last_score)
        elif choice == "3":
            leaders = load_scores()
            display_leaderboard(leaders)
        elif choice == "q":
            print("Goodbye!")
            break

