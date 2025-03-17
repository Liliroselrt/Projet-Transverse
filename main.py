import pygame
import pygame.freetype
import os

from components.game import Game, run_game
from utils.utils import *

# Initialisation de pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

running = True
show_menu = True
is_paused = False

background = pygame.image.load('./resources/background.jpeg')
background = pygame.transform.scale(background, (1280, 720))

pygame.freetype.init()
font_path = os.path.join('resources', 'fonts', 'AutourOne.ttf')
font = pygame.freetype.Font(font_path, 36)

if __name__ == "__main__":
    game = Game(screen.get_width(), screen.get_height())

    while running:
        # pygame.QUIT event means the user clicked X to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not show_menu:
                    is_paused = not is_paused
                    show_menu = is_paused
            if event.type == pygame.MOUSEBUTTONDOWN and show_menu:
                mouse_pos = event.pos
                if play_button.collidepoint(mouse_pos):
                    fade_out(screen, background)
                    show_menu = False
                    is_paused = False
                elif quit_button.collidepoint(mouse_pos):
                    running = False

        if show_menu:
            play_button, quit_button = draw_menu(screen, font, background)
        else:
            if not is_paused:
                screen.blit(background, (0, 0))

                # THE GAME IS HERE
                exit_requested = run_game(screen, clock)
                if exit_requested:
                    running = False
                show_menu = True

        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

    pygame.quit()
