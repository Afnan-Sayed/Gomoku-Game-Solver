import random
from gomoku import Gomoku

class GomokuGame:
    def __init__(self, size=15):
        self.board = Gomoku(size)
        self.current_player = 1  # Player 1 starts
        self.game_over = False
    
    def start_game(self):
        # Prompt the user for the game mode
        game_mode = input("Choose game mode:\n1. Human vs. AI\n2. AI vs. AI\nEnter your choice (1 or 2): ")
        
        if game_mode == "1":
            self.play_human_vs_ai()
        elif game_mode == "2":
            self.play_ai_vs_ai()
        else:
            print("Invalid choice, please enter 1 or 2.")
    
    def play_human_vs_ai(self):
        # Play Human vs. AI
        while not self.game_over:
            self.board.display_board()
            if self.current_player == 1:  # Human's turn
                self.human_move()
            else:  # AI's turn (plays randomly for now)
                self.ai_move()
            winner_start, winner_end = self.check_winner()
            if winner_start and winner_end:
                self.game_over = True
                print(f"Player {self.current_player} wins!")
                print(f"Winning move: {winner_start} to {winner_end}")
                self.display_winning_move(winner_start, winner_end)
            self.switch_turn()

    def play_ai_vs_ai(self):
        # Play AI vs. AI
        while not self.game_over:
            self.board.display_board()
            if self.current_player == 1:  # AI 1's turn
                self.ai_move()
            else:  # AI 2's turn
                self.ai_move()
            winner_start, winner_end = self.check_winner()
            if winner_start and winner_end:
                self.game_over = True
                print(f"Player {self.current_player} wins!")
                print(f"Winning move: {winner_start} to {winner_end}")
                self.display_winning_move(winner_start, winner_end)
            self.switch_turn()

    def human_move(self):
        while True:
            try:
                row, col = map(int, input("Enter your move (row, col): ").split(","))
                if self.board.update_board(row, col, self.current_player):
                    break
            except ValueError:
                print("Invalid input. Please enter row and column as numbers.")
            except IndexError:
                print("Move out of bounds. Please try again.")
    
    def ai_move(self):
        print("AI is making a move...")
        ai_row, ai_col = self.get_random_move()
        self.board.update_board(ai_row, ai_col, self.current_player)
    
    def get_random_move(self):
        # AI picks a random move (placeholder for Minimax/Alpha-Beta)
        empty_cells = [(i, j) for i in range(self.board.size) for j in range(self.board.size) if self.board.board[i][j] == 0]
        return random.choice(empty_cells) if empty_cells else (-1, -1)

    def check_winner(self):
        return self.board.check_winner()

    def display_winning_move(self, start, end):
        """Highlight the winning move on the board"""
        start_row, start_col = start
        end_row, end_col = end
        print("Winning sequence:")
        for r, c in self.get_winning_sequence(start_row, start_col, end_row, end_col):
            self.board.board[r][c] = 3  # Mark the winning cells with a special value (e.g., 3)
        self.board.display_board()

    def get_winning_sequence(self, start_row, start_col, end_row, end_col):
        """Generate the winning sequence of moves"""
        sequence = []
        if start_row == end_row:  # Horizontal win
            for col in range(start_col, end_col + 1):
                sequence.append((start_row, col))
        elif start_col == end_col:  # Vertical win
            for row in range(start_row, end_row + 1):
                sequence.append((row, start_col))
        else:  # Diagonal win
            row_step = 1 if start_row < end_row else -1
            col_step = 1 if start_col < end_col else -1
            for i in range(5):
                sequence.append((start_row + i * row_step, start_col + i * col_step))
        return sequence

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1
