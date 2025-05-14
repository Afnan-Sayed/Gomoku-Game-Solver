class Gomoku:
    def __init__(self, size=15):
        # Initialize the board as a 15x15 grid with all cells set to 0 (empty)
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
    
    def display_board(self):
        # Display the board in a human-readable format
        for row in self.board:
            print(" ".join(str(cell) if cell != 0 else "." for cell in row))
    
    def check_winner(self):
        # Check horizontal (5-in-a-row)
        for i in range(self.size):
            for j in range(self.size - 4):  # Ensure we don't go out of bounds
                if self.board[i][j] != 0 and \
                   self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3] == self.board[i][j+4]:
                    return (i, j), (i, j+4)  # Return the start and end position of the winning move

        # Check vertical (5-in-a-row)
        for i in range(self.size - 4):  # Only check until row 11 (to avoid out of bounds)
            for j in range(self.size):
                if self.board[i][j] != 0 and \
                   self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j] == self.board[i+4][j]:
                    return (i, j), (i+4, j)  # Return the start and end position of the winning move

        # Check diagonal (top-left to bottom-right)
        for i in range(self.size - 4):
            for j in range(self.size - 4):
                if self.board[i][j] != 0 and \
                   self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] == self.board[i+4][j+4]:
                    return (i, j), (i+4, j+4)  # Return the start and end position of the winning move

        # Check diagonal (top-right to bottom-left)
        for i in range(self.size - 4):
            for j in range(4, self.size):
                if self.board[i][j] != 0 and \
                   self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == self.board[i+3][j-3] == self.board[i+4][j-4]:
                    return (i, j), (i+4, j-4)  # Return the start and end position of the winning move

        return None, None  # No winner
    
    def update_board(self, row, col, player):
        """Update the board with the player's move"""
        if 0 <= row < self.size and 0 <= col < self.size:
            if self.board[row][col] == 0:  # Cell is empty
                self.board[row][col] = player
                return True
            else:
                print(f"Cell ({row},{col}) is already occupied.")
                return False
        else:
            print(f"Invalid position ({row},{col}). Must be between 0 and {self.size - 1}.")
            return False
