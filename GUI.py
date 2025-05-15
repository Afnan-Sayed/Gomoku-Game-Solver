import pygame
from Random.gomoku_game import GomokuGame  # Import your game logic class

# Initialize Pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Load sounds
start_sound = pygame.mixer.Sound("game-start-317318.mp3")
lets_go_sound = pygame.mixer.Sound("let's go.mp3")
sound_p1 = pygame.mixer.Sound("hit.mp3")
sound_p2 = pygame.mixer.Sound("hit.mp3")
win_sound = pygame.mixer.Sound("win.mp3")
lose_sound = pygame.mixer.Sound("lose.mp3")
crazy_font = pygame.font.SysFont("comicsansms", 60, bold=True)



size = 700
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("Gomoku Game")

board_size = 15
cell_size = 600 // board_size  # Board size fixed to 600x600 area inside window
board_area_top_left = (50, 50)  # Board offset from window edge

# Colors
BACKGROUND_COLOR = (200, 200, 200)  # Light grey outside board
LINE_COLOR = (0, 0, 0)
PLAYER_COLORS = {1: (0, 0, 0), 2: (255, 0, 0), 3: (0, 255, 0)}  # Black, Red, Green for winning highlight

# Load background image and scale to board size
board_bg_img = pygame.image.load("background.png")
board_bg_img = pygame.transform.scale(board_bg_img, (cell_size * board_size, cell_size * board_size))

# Instantiate the game logic
game = GomokuGame(size=board_size)

# Fonts for text
font = pygame.font.SysFont(None, 40)

def draw_start_screen():
    screen.fill((50, 50, 100))  # Background color of the start screen
    # Title text
    title_text = pygame.font.SysFont(None, 60).render("Welcome to Gomoku", True, (255, 255, 255))
    screen.blit(title_text, (size // 2 - title_text.get_width() // 2, size // 3 - 80))  # Center the title

    # Play button
    button_rect = pygame.Rect(size // 2 - 100, size // 2 - 40, 200, 80)
    pygame.draw.rect(screen, (0, 150, 0), button_rect)
    text = font.render("Play", True, (255, 255, 255))
    screen.blit(text, (button_rect.x + 70, button_rect.y + 20))
    pygame.display.flip()
    return button_rect

def draw_game_mode_screen():
    screen.fill((50, 50, 100))  # Background color for the game mode screen
    font_big = pygame.font.SysFont(None, 60)

    # Centered title text for Game Mode
    text = font_big.render("Choose Game Mode", True, (255, 255, 255))
    screen.blit(text, (size // 2 - text.get_width() // 2, size // 3 - 50))

    # Centered game mode options
    text1 = font.render("1. Human vs AI", True, (255, 255, 255))
    text2 = font.render("2. AI vs AI", True, (255, 255, 255))

    screen.blit(text1, (size // 2 - text1.get_width() // 2, size // 3 + 20))
    screen.blit(text2, (size // 2 - text2.get_width() // 2, size // 3 + 60))

    pygame.display.flip()

def draw_board():
    # Fill background outside board
    screen.fill(BACKGROUND_COLOR)
    # Draw board background image
    screen.blit(board_bg_img, board_area_top_left)

    # Draw grid lines on board area
    for i in range(board_size + 1):
        start_pos_h = (board_area_top_left[0] + i * cell_size, board_area_top_left[1])
        end_pos_h = (board_area_top_left[0] + i * cell_size, board_area_top_left[1] + cell_size * board_size)
        pygame.draw.line(screen, LINE_COLOR, start_pos_h, end_pos_h)
        start_pos_v = (board_area_top_left[0], board_area_top_left[1] + i * cell_size)
        end_pos_v = (board_area_top_left[0] + cell_size * board_size, board_area_top_left[1] + i * cell_size)
        pygame.draw.line(screen, LINE_COLOR, start_pos_v, end_pos_v)

    # Draw stones, including highlight for winning sequence (marked as 3)
    for r in range(game.board.size):
        for c in range(game.board.size):
            cell_value = game.board.board[r][c]
            if cell_value != 0:
                color = PLAYER_COLORS.get(cell_value, (0, 0, 0))
                center = (board_area_top_left[0] + c * cell_size + cell_size // 2,
                          board_area_top_left[1] + r * cell_size + cell_size // 2)
                pygame.draw.circle(screen, color, center, cell_size // 3)

def get_cell(pos):
    x, y = pos
    # Convert mouse position to board row, col considering board offset
    x_rel = x - board_area_top_left[0]
    y_rel = y - board_area_top_left[1]
    if 0 <= x_rel < cell_size * board_size and 0 <= y_rel < cell_size * board_size:
        col = x_rel // cell_size
        row = y_rel // cell_size
        return int(row), int(col)
    return None, None

# Opening screen loop
start_screen = True
play_button = draw_start_screen()
running = True  # define running here, so other loops can also use it

while start_screen and running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                start_screen = False
                start_sound.play()

# Game mode selection loop
game_mode_screen = True
mode = None  # Initialize mode here before the loop

while game_mode_screen and running:
    draw_game_mode_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_mode_screen = False
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if size // 2 - 100 <= mouse_x <= size // 2 + 100:
                if size // 3 + 20 <= mouse_y <= size // 3 + 60:  # Human vs AI
                    mode = "human_vs_ai"
                    game_mode_screen = False
                    lets_go_sound.play()
                elif size // 3 + 60 <= mouse_y <= size // 3 + 100:  # AI vs AI
                    mode = "ai_vs_ai"
                    game_mode_screen = False
                    lets_go_sound.play()

###############################################################################################################

def play_human_vs_ai():
    global running
    while running:
        draw_board()

        if game.game_over:
            if game.current_player == 2:  # AI won
                status_text = crazy_font.render("YOU LOST!", True, (255, 0, 0))
            else:
                status_text = font.render("You Win!", True, (0, 180, 0))
            text_x = size // 2 - status_text.get_width() // 2
            text_y = 10
            screen.blit(status_text, (text_x, text_y))
        else:
            status_text = font.render(f"Player {game.current_player}'s turn", True, (0, 0, 0))
            screen.blit(status_text, (10, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                if game.current_player == 1:  # Human turn
                    row, col = get_cell(pygame.mouse.get_pos())
                    if row is not None and col is not None:
                        moved = game.board.update_board(row, col, game.current_player)
                        if moved:
                            sound_p1.play()
                            start, end = game.check_winner()
                            if start is not None:
                                win_sound.play()
                                game.game_over = True
                            else:
                                game.switch_turn()

        # AI's turn automatically
        if not game.game_over and game.current_player == 2:
            pygame.time.wait(500)
            game.ai_move()
            sound_p2.play()
            start, end = game.check_winner()
            if start is not None:
                lose_sound.play()
                game.game_over = True
            else:
                game.switch_turn()


def play_ai_vs_ai():
    global running
    while running:
        draw_board()

        if game.game_over:
            status_text = font.render(f"Player {game.current_player} wins!", True, (255, 0, 0))
            screen.blit(status_text, (10, 10))
            pygame.display.flip()
            # Let the game pause a bit then quit or reset
            pygame.time.wait(3000)
            running = False
            break
        else:
            status_text = font.render(f"Player {game.current_player}'s turn", True, (0, 0, 0))
            screen.blit(status_text, (10, 10))
            pygame.display.flip()

        pygame.time.wait(500)  # Wait half a second between moves

        game.ai_move()
        if game.current_player == 1:
            sound_p1.play()
        else:
            sound_p2.play()

        start, end = game.check_winner()
        if start is not None:
            win_sound.play()
            game.game_over = True
        else:
            game.switch_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

# Main game loop
if mode == "human_vs_ai":
    play_human_vs_ai()
elif mode == "ai_vs_ai":
    play_ai_vs_ai()

pygame.quit()
