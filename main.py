from Random.gomoku_game import GomokuGame
""" 
here is handling gameplay loop, player turns, input/output, choosing between two models, and uses gomoku.py and ai.py to run the game

In main.py we will:

1. Initialize your board using gomoku.Gomoku().
2. Keep track of the current player.
3. For human moves, ask for user input and update the board.
4. For AI moves, call the AI algorithm function from Minimax.py or Alpha-Beta pruning.py, passing the current board state.
5. Update the board with the AI's chosen move.
6. Check if there is a winner.
7. Switch turns until the game ends.
"""

# Example of running the game:
if __name__ == "__main__":
    game = GomokuGame(size=15)
    game.start_game()


























"""
#SAMPLE-EXAMPLE
from Game_Rules.gomoku import Gomoku
from AI_Algo.Minimax import minimax  # assuming you have a minimax function here

def human_vs_ai():
    board = Gomoku()
    current_player = 1  # Human starts

    while True:
        board.display_board()

        if current_player == 1:
            # Human turn
            row, col = map(int, input("Enter your move (row,col): ").split(","))
            if board.update_board(row, col, current_player):
                current_player = 2
        else:
            # AI turn
            print("AI thinking...")
            ai_move = minimax(board, player=2)
            board.update_board(ai_move[0], ai_move[1], current_player)
            current_player = 1

        winner_start, winner_end = board.check_winner()
        if winner_start is not None:
            print(f"Player {current_player} wins!")
            board.display_board()
            break

def ai_vs_ai():
board = Gomoku()
current_player = 1

while True:
    board.display_board()
    print(f"AI Player {current_player} is thinking...")
    ai_move = minimax(board, player=current_player)
    board.update_board(ai_move[0], ai_move[1], current_player)

    winner_start, winner_end = board.check_winner()
    if winner_start is not None:
        print(f"Player {current_player} wins!")
        board.display_board()
        break

    current_player = 2 if current_player == 1 else 1

"""