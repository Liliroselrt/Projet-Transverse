import pygame
import pygame.freetype


def draw_blurred_background(screen, background):
    blurred_background = pygame.transform.smoothscale(background, (128, 72))
    blurred_background = pygame.transform.smoothscale(blurred_background, (1280, 720))
    screen.blit(blurred_background, (0, 0))


def draw_menu(screen, font, background):
    # Fond flouté
    draw_blurred_background(screen, background)

    # Dimensions et positions
    screen_width, screen_height = screen.get_size()
    modal_width = 600
    modal_height = 300
    modal_x = (screen_width - modal_width) // 2
    modal_y = (screen_height - modal_height) // 2

    # Modal avec coins arrondis et dégradé
    modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
    modal_surface = pygame.Surface((modal_width, modal_height), pygame.SRCALPHA)
    pygame.draw.rect(modal_surface, (20, 20, 20, 230), modal_surface.get_rect(), border_radius=15)
    screen.blit(modal_surface, modal_rect)

    # Titre du jeu
    title_font = pygame.freetype.Font(font.path, 64)
    title_surface, _ = title_font.render("Trash & Splash", (255, 255, 255))
    title_x = modal_x + (modal_width - title_surface.get_width()) // 2
    screen.blit(title_surface, (title_x, modal_y + 40))

    # Boutons
    button_width = 200
    button_height = 60
    spacing = 40

    # Bouton Jouer
    play_x = modal_x + (modal_width // 4) - (button_width // 2)
    play_y = modal_y + modal_height - button_height - 40
    play_button = pygame.Rect(play_x, play_y, button_width, button_height)
    pygame.draw.rect(screen, (46, 204, 113), play_button, border_radius=10)
    pygame.draw.rect(screen, (39, 174, 96), play_button, 2, border_radius=10)

    # Bouton Quitter
    quit_x = modal_x + (modal_width * 3 // 4) - (button_width // 2)
    quit_y = play_y
    quit_button = pygame.Rect(quit_x, quit_y, button_width, button_height)
    pygame.draw.rect(screen, (231, 76, 60), quit_button, border_radius=10)
    pygame.draw.rect(screen, (192, 57, 43), quit_button, 2, border_radius=10)

    # Texte des boutons centré
    jouer_text, _ = font.render("JOUER", (255, 255, 255))
    quitter_text, _ = font.render("QUITTER", (255, 255, 255))

    # Calcul des positions centrées
    jouer_text_x = play_x + (button_width - jouer_text.get_width()) // 2
    jouer_text_y = play_y + (button_height - jouer_text.get_height()) // 2

    quitter_text_x = quit_x + (button_width - quitter_text.get_width()) // 2
    quitter_text_y = quit_y + (button_height - quitter_text.get_height()) // 2

    # Rendu du texte centré
    screen.blit(jouer_text, (jouer_text_x, jouer_text_y))
    screen.blit(quitter_text, (quitter_text_x, quitter_text_y))

    return play_button, quit_button


def fade_out(screen, background):
    fade_surface = pygame.Surface((1280, 720))
    for alpha in range(255, -1, -5):
        screen.blit(background, (0, 0))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5)