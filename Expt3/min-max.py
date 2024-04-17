import math

# Constants for players
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

# Function to print the board
def print_board(board):
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
    print('-' * (4 * len(board) - 1))

# Function to check if a player wins
def check_winner(board, player):
    n = len(board)
    # Check rows and columns
    for i in range(n):
        if all(board[i][j] == player for j in range(n)) or all(board[j][i] == player for j in range(n)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(n)) or all(board[i][n-i-1] == player for i in range(n)):
        return True
    return False

# Function to check if the board is full
def is_board_full(board):
    return all(all(cell != EMPTY for cell in row) for row in board)

# Mini-Max algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    # Base cases
    if check_winner(board, PLAYER_X):
        return -1
    if check_winner(board, PLAYER_O):
        return 1
    if is_board_full(board):
        return 0

    if maximizing_player:
        max_eval = -math.inf
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta cut-off
        return max_eval
    else:
        min_eval = math.inf
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
        return min_eval

# Function to find the best moves using Mini-Max with alpha-beta pruning
def find_best_moves(board):
    best_moves = []
    best_eval = -math.inf
    alpha = -math.inf
    beta = math.inf
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_O
                eval = minimax(board, 0, alpha, beta, False)
                board[i][j] = EMPTY
                if eval > best_eval:
                    best_eval = eval
                    best_moves = [(i, j)]
                elif eval == best_eval:
                    best_moves.append((i, j))
                alpha = max(alpha, eval)
    return best_moves

# List to store the moves during the game
moves_list = []

# Function to make a move for the computer
def make_computer_move(board):
    best_moves = find_best_moves(board)
    for move in best_moves:
        print(f"Best move: (row: {move[0]}, col: {move[1]})")
    best_move = best_moves[0]  # Choose the first best move
    board[best_move[0]][best_move[1]] = PLAYER_O
    moves_list.append((best_move, PLAYER_O))

# Main game loop
def play_game():
    global moves_list
    n = int(input("Enter the board size N: "))
    board = [[EMPTY for _ in range(n)] for _ in range(n)]
    player = PLAYER_X

    while not check_winner(board, PLAYER_X) and not check_winner(board, PLAYER_O) and not is_board_full(board):
        print_board(board)

        if player == PLAYER_X:
            while True:
                try:
                    row, col = map(int, input("Player X (row, col): ").split())
                    if 0 <= row < n and 0 <= col < n and board[row][col] == EMPTY:
                        board[row][col] = PLAYER_X
                        moves_list.append(((row, col), PLAYER_X))
                        break
                    else:
                        print("Invalid move. Try again.")
                except (ValueError, IndexError):
                    print("Invalid input. Try again.")
        else:
            print("Computer's turn...")
            make_computer_move(board)

        player = PLAYER_O if player == PLAYER_X else PLAYER_X

    print_board(board)
    if check_winner(board, PLAYER_X):
        print("Player X wins!")
    elif check_winner(board, PLAYER_O):
        print("Player O wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()

    # Print the sequence of moves made during the game
    print("Move sequence:")
    for move, player in moves_list:
        print(f"{player} move: ({move[0]}, {move[1]})")
