import pygame
import sys
import pygame.freetype  # Importation de pygame.freetype pour charger les polices

"""Code pour l'affichage final : Victoire/défaite"""
"""Objectif : fenêtre avec un classement, le gagnant mis en avant"""

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
        winner_text, winner_rect = title_font.render("Joueur 2 Gagnant ! 🎉", (GREEN))
        player1_color = BLACK
        player2_color = GREEN
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




# Dimensions de la fenêtre du jeu
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jeu de pêche")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Vitesse de déplacement
speed = 5

# Joueur 1 (et 2)
joueur1_pos = [100, height // 2]
joueur2_pos = [width - 100, height // 2]


# Fonction pour afficher les informations du jeu
def afficher_jeu(joueur1_pos, joueur2_pos, nb_joueur):
    screen.fill(WHITE)

    # Dessiner les joueurs
    pygame.draw.rect(screen, BLACK, (joueur1_pos[0], joueur1_pos[1], 50, 50))  # Joueur 1
    if nb_joueur == 2:
        pygame.draw.rect(screen, (255, 0, 0), (joueur2_pos[0], joueur2_pos[1], 50, 50))  # Joueur 2

    pygame.display.flip()


# Fonction pour gérer les mouvements et actions
def gerer_evenements(nb_joueur):
    global joueur1_pos, joueur2_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if nb_joueur == 1:
                if event.key == pygame.K_UP:
                    joueur1_pos[1] -= speed
                if event.key == pygame.K_DOWN:
                    joueur1_pos[1] += speed
                if event.key == pygame.K_LEFT:
                    joueur1_pos[0] -= speed
                if event.key == pygame.K_RIGHT:
                    joueur1_pos[0] += speed
                if event.key == pygame.K_SPACE:
                    print("Joueur 1 utilise la canne à pêche")

            elif nb_joueur == 2:
                # Joueur 1 (gauche)
                if event.key == pygame.K_z:
                    joueur1_pos[1] -= speed
                if event.key == pygame.K_s:
                    joueur1_pos[1] += speed
                if event.key == pygame.K_q:
                    joueur1_pos[0] -= speed
                if event.key == pygame.K_d:
                    joueur1_pos[0] += speed
                if event.key == pygame.K_a:
                    print("Joueur 1 utilise la canne à pêche")

                # Joueur 2 (droite)
                if event.key == pygame.K_UP:
                    joueur2_pos[1] -= speed
                if event.key == pygame.K_DOWN:
                    joueur2_pos[1] += speed
                if event.key == pygame.K_LEFT:
                    joueur2_pos[0] -= speed
                if event.key == pygame.K_RIGHT:
                    joueur2_pos[0] += speed
                if event.key == pygame.K_m:
                    print("Joueur 2 utilise la canne à pêche")


# Choisir le nombre de joueurs et afficher le menu
def choisir_mode():
    while True:
        try:
            nb_joueur = int(input("Entrez le nombre de joueurs (1 ou 2) : "))
            if nb_joueur in [1, 2]:
                break
            else:
                choix_mode = int(input("Veuillez entrer 1 ou 2."))
                if choix_mode == 1:
                    mode_individuel()
                else :
                    mode_multijoueur()

        except ValueError:
            print("Veuillez entrer un nombre valide.")

    #afficher_menu_touches(nb_joueur)
    return nb_joueur


# Boucle principale du jeu
def main():
    nb_joueur = choisir_mode()

    # Boucle du jeu
    while True:
        gerer_evenements(nb_joueur)
        afficher_jeu(joueur1_pos, joueur2_pos, nb_joueur)

        pygame.time.delay(30)  # Petit délai pour contrôler la vitesse du jeu


if __name__ == "__main__":
    main()
