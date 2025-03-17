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
show_rules = False

# Chargement des images
background = pygame.image.load('resources/background.jpeg')
background = pygame.transform.scale(background, (1280, 720))

rules_background = pygame.image.load('resources/FondRegle.jpg')
rules_background = pygame.transform.scale(rules_background, (1280, 720))

# Chargement de la police
pygame.freetype.init()
font_path = os.path.join('resources', 'fonts', 'AutourOne.ttf')
font = pygame.freetype.Font(font_path, 36)


def draw_rules(screen, font):
    """ Affiche les règles du jeu et retourne le bouton retour. """
    screen.blit(rules_background, (0, 0))

    # Titre
    title_text, title_rect = font.render("Voici les règles du jeu :", (255, 255, 255))
    title_x = (1280 - title_rect.width) // 2
    screen.blit(title_text, (title_x, 100))

    # Liste des règles
    rules = [
        "1. Attraper les déchets pour sauver les poissons !",
        "2. Attention, ne pas attraper les poissons,\n",
        " sinon vous perdez des points.",
        "3. Gagnez le jeu en nettoyant l'océan !"
    ]

    y_base = 200
    for rule in rules:
        text_surface, rect = font.render(rule, (255, 255, 255))
        x = (1280 - rect.width) // 2
        screen.blit(text_surface, (x, y_base))
        y_base += 50

    # Bouton retour
    back_button = pygame.Rect(540, y_base + 50, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), back_button, border_radius=10)
    pygame.draw.rect(screen, (200, 0, 0), back_button, 2, border_radius=10)

    text_surface, _ = font.render("Retour", (255, 255, 255))
    text_x = back_button.x + (back_button.width - text_surface.get_width()) // 2
    text_y = back_button.y + (back_button.height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))

    return back_button


def draw_blurred_background(screen, background):
    """ Crée un effet de flou sur le fond """
    blurred_background = pygame.transform.smoothscale(background, (128, 72))
    blurred_background = pygame.transform.smoothscale(blurred_background, (1280, 720))
    screen.blit(blurred_background, (0, 0))


def draw_menu(screen, font):
    """ Affiche le menu principal avec les boutons Jouer, Quitter et Règles """
    draw_blurred_background(screen, background)

    # Fenêtre centrale
    modal_width = 600
    modal_height = 350
    modal_x = (1280 - modal_width) // 2
    modal_y = (720 - modal_height) // 2

    modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
    modal_surface = pygame.Surface((modal_width, modal_height), pygame.SRCALPHA)
    pygame.draw.rect(modal_surface, (20, 20, 20, 230), modal_surface.get_rect(), border_radius=15)
    screen.blit(modal_surface, modal_rect)

    # Titre du jeu
    title_font = pygame.freetype.Font(font.path, 60)
    title_surface, _ = title_font.render("Trash & Splash", (255, 255, 255))
    title_x = modal_x + (modal_width - title_surface.get_width()) // 2
    screen.blit(title_surface, (title_x, modal_y + 20))

    # Dimensions des boutons
    button_width = 200
    button_height = 60
    spacing = 20

    # Ajuster la position des boutons pour laisser de la place au titre
    title_height = title_surface.get_height()
    first_button_y = modal_y + title_height + 40  # Laisser de l'espace après le titre

    # Bouton Jouer
    play_button = pygame.Rect(modal_x + (modal_width - button_width) // 2, first_button_y, button_width, button_height)
    pygame.draw.rect(screen, (46, 204, 113), play_button, border_radius=10)

    # Bouton Règles
    rules_button = pygame.Rect(modal_x + (modal_width - button_width) // 2, first_button_y + button_height + spacing, button_width, button_height)
    pygame.draw.rect(screen, (52, 152, 219), rules_button, border_radius=10)

    # Bouton Quitter
    quit_button = pygame.Rect(modal_x + (modal_width - button_width) // 2, first_button_y + 2 * (button_height + spacing), button_width, button_height)
    pygame.draw.rect(screen, (231, 76, 60), quit_button, border_radius=10)

    # Texte des boutons
    jouer_text, _ = font.render("JOUER", (255, 255, 255))
    regles_text, _ = font.render("RÈGLES", (255, 255, 255))
    quitter_text, _ = font.render("QUITTER", (255, 255, 255))

    # Affichage du texte centré dans chaque bouton
    screen.blit(jouer_text, (play_button.x + (button_width - jouer_text.get_width()) // 2,
                             play_button.y + (button_height - jouer_text.get_height()) // 2))
    screen.blit(regles_text, (rules_button.x + (button_width - regles_text.get_width()) // 2,
                              rules_button.y + (button_height - regles_text.get_height()) // 2))
    screen.blit(quitter_text, (quit_button.x + (button_width - quitter_text.get_width()) // 2,
                               quit_button.y + (button_height - quitter_text.get_height()) // 2))

    return play_button, rules_button, quit_button




if __name__ == "__main__":
    while running:
        screen.fill((0, 0, 0))  # Efface l'écran avant de dessiner
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                show_menu = True
                show_rules = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_menu:
                    play_button, rules_button, quit_button = draw_menu(screen, font)

                    if play_button.collidepoint(event.pos):
                        show_menu = False  # Ajouter ici le lancement du jeu
                    elif rules_button.collidepoint(event.pos):
                        show_menu = False
                        show_rules = True
                    elif quit_button.collidepoint(event.pos):
                        running = False

                elif show_rules:
                    back_button = draw_rules(screen, font)
                    if back_button.collidepoint(event.pos):
                        show_rules = False
                        show_menu = True

        if show_menu:
            draw_menu(screen, font)
        elif show_rules:
            draw_rules(screen, font)
        else :
            screen.blit(background, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
