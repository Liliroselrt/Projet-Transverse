import pygame
import sys
import pygame.freetype  # Importation de pygame.freetype pour charger les polices

# Initialisation de pygame
pygame.init()

# Définir les dimensions de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu 2D - Écran de Victoire")

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Charger la police (remplace "path/to/your/font.ttf" par le chemin de ta police)
title_font = pygame.freetype.Font("path/to/your/font.ttf", 60)
medium_font = pygame.freetype.Font("path/to/your/font.ttf", 40)


# Fonction pour afficher l'écran de victoire
def display_victory_screen(score1, score2):
    screen.fill(WHITE)

    # Titre de la victoire
    title_text, title_rect = title_font.render("Félicitations !", (YELLOW))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_rect.width // 2, 150))

    # Vérifier qui a gagné
    if score1 > score2:
        # Si Joueur 1 gagne
        winner_text, winner_rect = title_font.render("Joueur 1 Gagnant ! 🎉", (GREEN))
        player1_color = GREEN
        player2_color = BLACK
    elif score2 > score1:
        # Si Joueur 2 gagne
        winner_text, winner_rect = title_font.render("Joueur 2 Gagnant ! 🎉", (BLUE))
        player1_color = BLACK
        player2_color = BLUE
    else:
        # Si match nul
        winner_text, winner_rect = title_font.render("Match Nul !", (BLACK))
        player1_color = BLACK
        player2_color = BLACK

    # Afficher le message de victoire du gagnant (centré)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_rect.width // 2, 250))

    # Afficher les scores
    if score1 > score2:
        # Afficher le score du gagnant (Joueur 1)
        player1_text, player1_rect = title_font.render(f"Joueur 1: {score1}", (player1_color))
        player2_text, player2_rect = medium_font.render(f"Joueur 2: {score2}", (player2_color))
    elif score2 > score1:
        # Afficher le score du gagnant (Joueur 2)
        player2_text, player2_rect = title_font.render(f"Joueur 2: {score2}", (player2_color))
        player1_text, player1_rect = medium_font.render(f"Joueur 1: {score1}", (player1_color))
    else:
        # Si match nul, afficher les scores de façon équivalente
        player1_text, player1_rect = medium_font.render(f"Joueur 1: {score1}", (player1_color))
        player2_text, player2_rect = medium_font.render(f"Joueur 2: {score2}", (player2_color))

    # Afficher les scores à des positions différentes
    screen.blit(player1_text, (SCREEN_WIDTH // 4 - player1_rect.width // 2, 350))
    screen.blit(player2_text, (3 * SCREEN_WIDTH // 4 - player2_rect.width // 2, 350))

    # Instructions de bouton
    replay_text, replay_rect = medium_font.render("Appuyez sur 'R' pour rejouer", (YELLOW))
    quit_text, quit_rect = medium_font.render("Appuyez sur 'Q' pour quitter", (YELLOW))
    screen.blit(replay_text, (SCREEN_WIDTH // 2 - replay_rect.width // 2, 450))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_rect.width // 2, 500))

    # Afficher les changements à l'écran
    pygame.display.flip()


# Fonction principale
def main():
    # Attends que la logique de jeu te fournisse les scores des deux joueurs
    # Exemple : score1 = joueur1.get_score() et score2 = joueur2.get_score()

    # Afficher l'écran de victoire avec les scores des joueurs
    # Remplace les scores par les valeurs réelles du jeu
    score1 = 0  # Remplacer par le score réel de Joueur 1
    score2 = 0  # Remplacer par le score réel de Joueur 2
    display_victory_screen(score1, score2)

    # Boucle d'événements
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Rejouer
                    print("Rejouer !")  # Ajouter la logique de relance du jeu ici
                    return
                if event.key == pygame.K_q:  # Quitter
                    pygame.quit()
                    sys.exit()


# Démarrer le jeu
if __name__ == "__main__":
    main()
