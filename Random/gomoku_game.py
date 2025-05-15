import random
from Rules.gomoku import Gomoku

class GomokuGame:
    def __init__(self, size=15, depth=2):
        self.board = Gomoku(size)
        self.current_player = 1  # Player 1 starts not the AI if AI will rep 2
        self.game_over = False
        self.max_depth = depth

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
            else:  #
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
                self.ai_move_alphaBeta()
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
        print("AI Minimax is making a move...")
        best_score = float('-inf')
        best_move = None

        # Focus only on cells that are adjacent to existing pieces to reduce branching factor
        moves_to_check = self.get_adjacent_empty_cells()

        # If no adjacent cells (first move), choose a cell near the center
        if not moves_to_check:
            center = self.board.size // 2
            self.board.update_board(center, center, self.current_player)
            return

        for row, col in moves_to_check:
            self.board.board[row][col] = self.current_player  # 5,5
            score = self.minimax(0, False)  # score is good 0 is depth
            self.board.board[row][col] = 0  # undo

            if score > best_score:
                best_score = score
                best_move = (row, col)

        ai_row, ai_col = best_move
        self.board.update_board(ai_row, ai_col, self.current_player)

    def ai_move_alphaBeta(self):
        print("AI Alpha_Beta is making a move...")
        best_score = float('-inf')
        best_move = None

        moves_to_check = self.get_adjacent_empty_cells()

        if not moves_to_check:  # If no adjacent cells, pick the center (first move)
            center = self.board.size // 2
            self.board.update_board(center, center, self.current_player)
            return

        for row, col in moves_to_check:
            self.board.board[row][col] = self.current_player  # Make the move
            score = self.alpha_beta(0, float('-inf'), float('inf'), False)  # Call Alpha-Beta with depth 0
            self.board.board[row][col] = 0  # Undo the move

            if score > best_score:
                best_score = score
                best_move = (row, col)

        ai_row, ai_col = best_move
        self.board.update_board(ai_row, ai_col, self.current_player)  # Apply the best move

    def get_adjacent_empty_cells(self):
        adjacent_cells = set()
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] != 0:  # If cell has a piece
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if (0 <= ni < self.board.size and
                                    0 <= nj < self.board.size and
                                    self.board.board[ni][nj] == 0):
                                adjacent_cells.add((ni, nj))
        return list(adjacent_cells)

    def minimax(self, depth, is_maximizing):
        # Check if game is over or maximum depth reached
        winner_start, winner_end = self.check_winner()  # 1,1 #1,5
        if winner_start and winner_end:
            return 100 if self.board.board[winner_start[0]][winner_start[1]] == self.current_player else -100
        # base case2
        if depth == self.max_depth:
            return self.evaluate_board()

        if is_maximizing:
            max_eval = float('-inf')
            moves = self.get_adjacent_empty_cells()

            for row, col in moves:
                if self.board.board[row][col] == 0:
                    self.board.board[row][col] = self.current_player  # 2,3
                    eval = self.minimax(depth + 1, False)
                    self.board.board[row][col] = 0  # undo
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            moves = self.get_adjacent_empty_cells()

            opponent = 1 if self.current_player == 2 else 2
            for row, col in moves:
                if self.board.board[row][col] == 0:
                    self.board.board[row][col] = opponent
                    eval = self.minimax(depth + 1, True)
                    self.board.board[row][col] = 0
                    min_eval = min(min_eval, eval)
            return min_eval

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        # Base case: check if game over or maximum depth is reached
        winner_start, winner_end = self.check_winner()
        if winner_start and winner_end:
            return 100 if self.board.board[winner_start[0]][winner_start[1]] == self.current_player else -100
        if depth == self.max_depth:
            return self.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')  # Start with a very low score
            moves = self.get_adjacent_empty_cells()

            for row, col in moves:
                self.board.board[row][col] = self.current_player  # Try the move
                eval = self.alpha_beta(depth + 1, alpha, beta, False)  # Explore opponent's move
                self.board.board[row][col] = 0  # Undo the move

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)  # Update alpha (max value for maximizing player)

                if beta <= alpha:  # Beta cut-off (pruning)
                    break  # No need to explore further; prune this branch

            return max_eval
        else:
            min_eval = float('inf')  # Start with a very high score
            moves = self.get_adjacent_empty_cells()

            opponent = 2 if self.current_player == 1 else 1
            for row, col in moves:
                self.board.board[row][col] = opponent  # Try the opponent's move
                eval = self.alpha_beta(depth + 1, alpha, beta, True)  # Explore AI's move
                self.board.board[row][col] = 0  # Undo the move

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)  # Update beta (min value for minimizing player)

                if beta <= alpha:  # Alpha cut-off (pruning)
                    break  # No need to explore further; prune this branch

            return min_eval

    def evaluate_board(self):
        score = 0
        # Check horizontal, vertical, and diagonal lines
        # up     right  down     dig down
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] == 0:
                    continue

                is_current_player = self.board.board[i][j] == self.current_player
                player_factor = 1 if is_current_player else -1

                for dr, dc in directions:
                    streak_length = 0
                    open_ends = 0

                    # Check if space before streak is empty
                    prev_r, prev_c = i - dr, j - dc
                    if 0 <= prev_r < self.board.size and 0 <= prev_c < self.board.size:
                        if self.board.board[prev_r][prev_c] == 0:
                            open_ends += 1

                    # Calculate streak length
                    for k in range(5):
                        r, c = i + k * dr, j + k * dc
                        if not (0 <= r < self.board.size and 0 <= c < self.board.size):
                            break
                        if self.board.board[r][c] != self.board.board[i][j]:
                            break
                        streak_length += 1

                    # Check if space after streak is empty
                    next_r, next_c = i + streak_length * dr, j + streak_length * dc
                    if 0 <= next_r < self.board.size and 0 <= next_c < self.board.size:
                        if self.board.board[next_r][next_c] == 0:
                            open_ends += 1

                    # Score based on streak length and open ends
                    if streak_length >= 5:
                        return 100 * player_factor
                    elif streak_length == 4:
                        if open_ends == 2:
                            score += 50 * player_factor
                        elif open_ends == 1:
                            score += 10 * player_factor
                    elif streak_length == 3:
                        if open_ends == 2:
                            score += 5 * player_factor
                        elif open_ends == 1:
                            score += 2 * player_factor
                    elif streak_length == 2:
                        if open_ends == 2:
                            score += 1 * player_factor
        return score

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