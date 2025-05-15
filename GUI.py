#window, game loop, event handler
import pygame
# from Rules import gomoku
# from Random import gomoku_game

pygame.init()

#window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#game loop
run = True
while run:
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()