import pygame
import pygame.freetype
import os
from utils.utils import *

from components.game import run_game


def handle_name_input(screen, font, nb_joueur):
    """Gère la saisie des noms des joueurs."""

    # Champs de saisie
    input_box1 = pygame.Rect(440, 250, 400, 60)  # Champ Joueur 1
    input_box2 = pygame.Rect(440, 350, 400, 60)  # Champ Joueur 2 (si 2 joueurs)

    active1 = True  # Indique si le champ 1 est actif
    active2 = False  # Indique si le champ 2 est actif (pour 2 joueurs)

    player1_name = ""
    player2_name = ""

    color_inactive = (100, 100, 100)
    color_active = (0, 150, 0)
    color1 = color_active
    color2 = color_inactive

    running = True
    while running:
        screen.fill((255, 255, 255))  # Nettoyer l'écran

        # Affichage du titre
        title_text, _ = font.render("Entrez les noms des joueurs", (0, 0, 0))
        screen.blit(title_text, (440, 100))

        # Dessiner les champs de texte
        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.draw.rect(screen, color2, input_box2,
                         2 if nb_joueur == 2 else 0)  # Afficher input 2 seulement si 2 joueurs

        # Afficher les noms saisis
        text_surface1 = font.render(player1_name, True, (0, 0, 0))
        screen.blit(text_surface1, (input_box1.x + 10, input_box1.y + 15))

        if nb_joueur == 2:
            text_surface2 = font.render(player2_name, True, (0, 0, 0))
            screen.blit(text_surface2, (input_box2.x + 10, input_box2.y + 15))

        # Bouton de validation
        start_button = pygame.Rect(440, 450, 200, 60)
        pygame.draw.rect(screen, (46, 204, 113), start_button, border_radius=10)
        start_text, _ = font.render("Commencer", (255, 255, 255))
        screen.blit(start_text, (start_button.x + 50, start_button.y + 15))

        pygame.display.flip()  # Mettre à jour l'écran

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None  # Quitter proprement

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier si on clique sur un champ
                if input_box1.collidepoint(event.pos):
                    active1 = True
                    active2 = False
                elif input_box2.collidepoint(event.pos) and nb_joueur == 2:
                    active1 = False
                    active2 = True
                else:
                    active1 = active2 = False

                # Mise à jour des couleurs
                color1 = color_active if active1 else color_inactive
                color2 = color_active if active2 else color_inactive

                # Vérifier si on clique sur le bouton de validation
                if start_button.collidepoint(event.pos):
                    return player1_name, player2_name  # Retourner les noms saisis

            if event.type == pygame.KEYDOWN:
                # Saisie pour le champ actif
                if active1:
                    if event.key == pygame.K_RETURN:
                        active1 = False
                        active2 = True if nb_joueur == 2 else False
                    elif event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    else:
                        player1_name += event.unicode

                elif active2:
                    if event.key == pygame.K_RETURN:
                        return player1_name, player2_name
                    elif event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    else:
                        player2_name += event.unicode

        pygame.time.Clock().tick(30)  # Limite à 30 FPS

    return player1_name, player2_name

def draw_player_selection(screen, font):
    """ Affiche l'écran pour choisir le nombre de joueurs et leurs commandes """
    screen.fill((255, 255, 255))  # Remplir l'écran avec du blanc pour ce menu

    # Dimensions et positions
    screen_width, screen_height = screen.get_size()
    modal_width = 600
    modal_height = 300
    modal_x = (screen_width - modal_width) // 2
    modal_y = (screen_height - modal_height) // 2

    # Affichage du titre
    title_text, title_rect = font.render("Sélectionner le nombre de joueurs", (0, 0, 0))
    title_x = (1280 - title_rect.width) // 2
    screen.blit(title_text, (title_x, 100))


    # Bouton 1 Joueur
    #one_player_button = pygame.Rect(modal_x + (modal_width - button_width) // 2, first_button_y, button_width,
    #                              button_height)
    #pygame.draw.rect(self.screen, (46, 204, 113), play_button, border_radius=10)


    #self.screen.blit(jouer_text, (play_button.x + (button_width - jouer_text.get_width()) // 2,
    #                          play_button.y + (button_height - jouer_text.get_height()) // 2))

    # Bouton 2 Joueurs
    two_players_button = pygame.Rect(440, 350, 400, 60)
    pygame.draw.rect(screen, (52, 152, 219), two_players_button, border_radius=10)
    two_players_text, _ = font.render("2 Joueurs", (255, 255, 255))
    screen.blit(two_players_text, (two_players_button.x + (two_players_button.width - two_players_text.get_width()) // 2,
                                  two_players_button.y + (two_players_button.height - two_players_text.get_height()) // 2))

    pygame.display.flip()

    return """one_player_button""""", two_players_button
