import pygame.freetype
from utils.utils import *
from components.menu import Menu
import os

from utils.video import start_video


def main():
    # Initialise Pygame
    pygame.init()

    # Récupérer la résolution de l'écran du joueur
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    # Dimensions standardisées pour tout le jeu
    WIDTH, HEIGHT = 1280, 720

    # Calculer la position pour centrer la fenêtre
    os_x = (screen_width - WIDTH) // 2
    os_y = (screen_height - HEIGHT) // 2

    # Définir la position de la fenêtre et la créer
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{os_x},{os_y}"
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Trash & Splash")
    clock = pygame.time.Clock()

    start_video(screen, clock, WIDTH, HEIGHT)

    # Affiche le menu
    Menu(screen, clock).run()

    pygame.quit()


if __name__ == "__main__":
    main()
