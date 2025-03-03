import pygame
import pygame.freetype
import os
from utils.utils import *

# Initialisation de pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

running = True
show_menu = True

background = pygame.image.load('./resources/background.png')
background = pygame.transform.scale(background, (1280, 720))

pygame.freetype.init()
font_path = os.path.join('resources', 'fonts', 'AutourOne.ttf')
font = pygame.freetype.Font(font_path, 36)

if __name__ == "__main__":
    while running:
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and show_menu:
                mouse_pos = event.pos
                if play_button.collidepoint(mouse_pos):
                    fade_out(screen, background)
                    show_menu = False
                elif quit_button.collidepoint(mouse_pos):
                    running = False

        if show_menu:
            play_button, quit_button = draw_menu(screen, font, background)
        else:
            screen.blit(background, (0, 0))
            # TODO: RENDER THE GAME HERE

        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

    pygame.quit()
