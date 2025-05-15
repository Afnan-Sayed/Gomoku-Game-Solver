from Random.gomoku_game import GomokuGame

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