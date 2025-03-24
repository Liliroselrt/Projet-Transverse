import pygame
import numpy as np

# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lancer de Canne à Pêche")
clock = pygame.time.Clock()

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


# Bibliothèque de gravité par niveau
def get_gravity(level):
    gravity_levels = {1: 9.81, 2: 12.0, 3: 15.0, 4: 18.0, 5: 21.0}
    return gravity_levels.get(level, 9.81)


# Simulation du lancer
def lancer_canne(angle, gravity):
    g = gravity
    v0 = 10
    angle_rad = np.radians(angle)

    t_max = (2 * v0 * np.sin(angle_rad)) / g
    t = np.linspace(0, t_max, num=50)

    x = v0 * np.cos(angle_rad) * t
    y = v0 * np.sin(angle_rad) * t - 0.5 * g * t ** 2

    return x, y

# Conversion des coordonnées en pixels
scale = 50
x_pixels = x * scale
y_pixels = HEIGHT - (y * scale)


def sauvegarder_scores(joueur, score):
    """Sauvegarde les scores des joueurs dans un fichier texte."""
    with open("scores.txt", "a") as file:
        file.write(f"Joueur {joueur} - Score: {score}\n")


def main():
    scores = []
    for joueur in range(1, 3):
        score = int(input(f"Joueur {joueur}, entrez votre score : "))
        sauvegarder_scores(joueur, score)
        scores.append((joueur, score))

    print("Scores sauvegardés !")


if __name__ == "__main__":
    main()

