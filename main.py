import pygame
import pygame.freetype
from utils.utils import *
import cv2
from components.menu import Menu
from AffichageFinal import affichage_final


def main():
    # Initialise Pygame

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Trash & Splash")
    clock = pygame.time.Clock()

    # Recherche vidéo
    cap = cv2.VideoCapture("resources/animation/animation.mpg")

    # Afficher la vidéo
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break
        frame = cv2.resize(frame, (1280, 720))

        # Bonne gestion des couleurs
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")

        # Gestion de l'image
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

    cap.release() # Arret de la vidéo

    # Affiche le menu
    Menu(screen, clock).run()

    pygame.quit()


if __name__ == "__main__":
    main()
