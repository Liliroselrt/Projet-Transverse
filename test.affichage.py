import pygame
import sys

from AffichageFinal import affichage_final

def test_affichage_final():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test écran de fin")


    players = [
        {'name': 'Alice', 'score': 100},
        {'name': 'Bob', 'score': 200},
    ]

# Appelle directement l'écran de fin
    affichage_final(screen, players)

# Quitte pygame correctement après l'écran de fin
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_affichage_final()
