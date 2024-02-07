import math

def display_board(board):
    for row in board:
        print(' | '.join(row))
        print('-' * (4 * len(row) - 1))

def is_terminal(state):
    if check_win(state, "X"):
        return True
    elif check_win(state, "O"):
        return True
    elif all(all(cell != " " for cell in row) for row in state):
        return True
    return False


def evaluate(state):
    if check_win(state, "X"):
        return -1 
    elif check_win(state, "O"):
        return 1   # AI wins
    else:
        return 0   # Draw

def generate_moves(state):
    moves = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == " ":
                new_state = [row.copy() for row in state]
                new_state[i][j] = "X" if is_player_turn(state) else "O"
                moves.append(new_state)
    return moves

def is_player_turn(state):
    count_x = sum(row.count("X") for row in state)
    count_o = sum(row.count("O") for row in state)
    return count_x == count_o

def check_win(state, player):
    # Check if the specified player has won
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(state[i][j] == player for j in range(3)) or all(state[j][i] == player for j in range(3)):
            return True
    if all(state[i][i] == player for i in range(3)) or all(state[i][2 - i] == player for i in range(3)):
        return True
    return False

def get_human_move(board):
    while True:
        row, col = map(int, input(f"Enter row and column (0 - {len(board) - 1}) separated by space: ").split())
        if board[row][col] == ' ':
            board[row][col] = 'X'
            return
        else:
            print("Invalid move! Cell is already occupied. Try again")

def minimax_alpha_beta_pruning(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(state):
        return evaluate(state)

    if maximizing_player:
        max_eval = -math.inf
        for child_state in generate_moves(state):
            eval_score = minimax_alpha_beta_pruning(child_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return max_eval
    else:
        min_eval = math.inf
        for child_state in generate_moves(state):
            eval_score = minimax_alpha_beta_pruning(child_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return min_eval
        
def get_move_indices(board, move):
    for i in range(3):
        for j in range(3):
            if board[i][j] != move[i][j]:
                return i, j
    return -1, -1  # R
    
def main():
    n = -1 # dimension of the board
    
    # Board size should be at least 3*3
    while n < 3:
        n = int(input("Enter the board size (n): "))
    
    board = [[' ' for _ in range(n)] for _ in range(n)]
    
    display_board(board)

    while not is_terminal(board):
        # Human player's move
        get_human_move(board)
        display_board(board)

        # if someone has won
        if is_terminal(board):
            break

        # Minimax AI player's move
        depth = 4  # Adjust the depth as needed
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True

        best_move = None
        best_score = -math.inf
        
        for move in generate_moves(board):
           eval_score = minimax_alpha_beta_pruning(move, depth - 1, alpha, beta, not maximizing_player)
           if eval_score > best_score:
                best_score = eval_score
                best_move = move  # Use the move from the loop

        # Now, use best_move to update the board
        row, col = get_move_indices(board, best_move)
        if row == -1 or col == -1:
            print("Invalid move!")
            break
        board[row][col] = "O"


        print("AI player's move:")
        display_board(board)

    print("Game Over!")
    
    display_board(board)

    if check_win(board, "X"):
       print("You win!")
    elif check_win(board, "O"):
       print("AI wins!")
    else:
       print("It's a draw!")


if __name__ == "__main__":
    main()
