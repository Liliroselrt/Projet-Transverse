import pygame
import pygame.freetype
import os

from components.game import Game, run_game
from utils.utils import *

from components.menu import Menu


def main():
    # Initialise Pygame
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Trash & Splash")
    clock = pygame.time.Clock()

    # Affiche le menu
    menu = Menu(screen, clock)
    quit_game = menu.run()

    # Clean up
    pygame.quit()


if __name__ == "__main__":
    main()
