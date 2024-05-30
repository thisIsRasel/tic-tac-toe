"""
Heuristics:
1) Win: If the AI can win in the current move, it should do so.
2) Block: If the opponent can win in the next move, the AI should block it.
3) Center: Take the center square if available.
4) Opposite Corner: If the opponent is in a corner, take the opposite corner.
5) Empty Corner: Take any of the available corners.
6) Empty Side: Take any of the available sides.
"""

import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    for row in board:
        if all([spot == player for spot in row]):
            return True
        
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
        
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    
    return False

def get_empty_positions(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def apply_heuristic(board, player):
    opponent = "O" if player == "X" else "X"
    
    # Win
    for (i, j) in get_empty_positions(board):
        board[i][j] = player
        if check_winner(board, player):
            return (i, j)
        board[i][j] = " "
    
    # Block
    for (i, j) in get_empty_positions(board):
        board[i][j] = opponent
        if check_winner(board, opponent):
            board[i][j] = player
            return (i, j)
        board[i][j] = " "
    
    # Take center
    if board[1][1] == " ":
        return (1, 1)
    
    # Take corners
    for (i, j) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[i][j] == " ":
            return (i, j)
    
    # Take sides
    for (i, j) in [(0, 1), (1, 0), (1, 2), (2, 1)]:
        if board[i][j] == " ":
            return (i, j)
    
    # Random move (should not happen in a complete heuristic setup)
    return random.choice(get_empty_positions(board))

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    
    while get_empty_positions(board):
        print_board(board)
        if current_player == "X":
            i, j = map(int, input("Enter your move (row col): ").split())

            if board[i][j] != " ":
                print("Invalid move. Try again.")
                continue
        else:
            i, j = apply_heuristic(board, current_player)
            print(f"AI ({current_player}) plays: {i} {j}")
        
        if board[i][j] == " ":
            board[i][j] = current_player
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                return
            
        current_player = "O" if current_player == "X" else "X"
    
    print_board(board)
    print("It's a draw!")

if __name__ == "__main__":
    main()