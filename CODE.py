import pygame

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Menu du Jeu")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)

# Police
font = pygame.font.Font(None, 50)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Boucle du menu
menu_running = True
while menu_running:
    fenetre.fill(BLANC)
    draw_text("Menu du Jeu", font, NOIR, fenetre, largeur // 2, 100)
    draw_text("1. Jouer", font, VERT, fenetre, largeur // 2, 250)
    draw_text("2. Quitter", font, ROUGE, fenetre, largeur // 2, 350)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("Démarrer le jeu (logique à implémenter)")
                menu_running = False  # Remplacez ceci par le lancement du jeu
            elif event.key == pygame.K_2:
                menu_running = False

# Quitter proprement
pygame.quit()