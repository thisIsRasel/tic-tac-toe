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

class TicTacToe:

    def __init__(self) -> None:
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def set_move(self, index):
        self.board[index//3][index%3] = self.current_player
        self.change_player()

    def get_move(self):
        i, j = self.apply_heuristic(self.current_player)
        return i*3 + j
    
    def change_player(self):
        if self.current_player == "O":
            self.current_player = "X"
        else:
            self.current_player = "O"

    def check_winner(self, player) -> bool:
        for row in self.board:
            if all([spot == player for spot in row]):
                return True
            
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return True
            
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        
        return False

    def get_empty_positions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]

    def apply_heuristic(self, player):
        opponent = "O" if player == "X" else "X"
        
        # Win
        for (i, j) in self.get_empty_positions():
            self.board[i][j] = player
            if self.check_winner(player):
                return (i, j)
            self.board[i][j] = " "
        
        # Block
        for (i, j) in self.get_empty_positions():
            self.board[i][j] = opponent
            if self.check_winner(opponent):
                self.board[i][j] = player
                return (i, j)
            self.board[i][j] = " "
        
        # Take center
        if self.board[1][1] == " ":
            return (1, 1)
        
        # Take corners
        for (i, j) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            if self.board[i][j] == " ":
                return (i, j)
        
        # Take sides
        for (i, j) in [(0, 1), (1, 0), (1, 2), (2, 1)]:
            if self.board[i][j] == " ":
                return (i, j)
        
        # Random move (should not happen in a complete heuristic setup)
        return random.choice(self.get_empty_positions())