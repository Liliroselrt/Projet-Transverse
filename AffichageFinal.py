import pygame
import pygame.freetype
import sys
import random

pygame.init()
pygame.freetype.init()

# Définir les dimensions de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu 2D - Écran de Victoire")

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
GRAY = (200, 200, 200)

background = pygame.image.load('resources/assets/images/background.jpeg')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonction pour dessiner le texte avec une ombre
def draw_text_with_shadow(surface, text, font, color, x, y, shadow_color=BLACK, offset=2):
    shadow = font.render(text, True, shadow_color)
    surface.blit(shadow, (x + offset, y + offset))
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Classe pour les confettis
class Confetti:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-50, -10)
        self.radius = random.randint(5, 10)
        self.color = random.choice([(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)])
        self.speed = random.uniform(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

def affichage_final(screen, players):
    font_title = pygame.font.SysFont(None, 80)
    font_text = pygame.font.SysFont(None, 50)

    # Détecte gagnant si 2 joueurs
    winner = None
    if len(players) == 2:
        if players[0]['score'] > players[1]['score']:
            winner = players[0]
        elif players[1]['score'] > players[0]['score']:
            winner = players[1]
        else:
            winner = None  # Égalité

    clock = pygame.time.Clock()
    running = True

    # Liste des confettis
    confettis = [Confetti() for _ in range(100)]

    # Animation pulsation
    pulse_scale = 1.0
    pulse_direction = 1

    while running:
        screen.blit(background, (0, 0))

        # Met à jour les confettis
        for confetti in confettis:
            confetti.update()
            confetti.draw(screen)

        # Titre
        title_text = "🎉 Fin du jeu ! 🎉"
        title_surface = font_title.render(title_text, True, WHITE)
        draw_text_with_shadow(screen, title_text, font_title, WHITE,
                              screen.get_width() // 2 - title_surface.get_width() // 2, 50)

        # Affichage des scores
        y_offset = 200
        for player in players:
            if (winner and player == winner) or (len(players) == 1):  # Gagnant ou joueur solo
                text = f"🏆 {player['name']} : {player['score']} pts"

                # Pulsation
                scale_font = pygame.font.SysFont(None, int(50 * pulse_scale))
                text_size = scale_font.size(text)
                draw_text_with_shadow(screen, text, scale_font, GOLD,
                                      screen.get_width() // 2 - text_size[0] // 2, y_offset)
            else:
                text = f"{player['name']} : {player['score']} pts"
                draw_text_with_shadow(screen, text, font_text, GRAY,
                                      screen.get_width() // 2 - font_text.size(text)[0] // 2, y_offset)
            y_offset += 80

        # Instructions pour quitter
        quit_text = "Appuyez sur une touche pour quitter"
        draw_text_with_shadow(screen, quit_text, font_text, WHITE,
                              screen.get_width() // 2 - font_text.size(quit_text)[0] // 2, screen.get_height() - 100)

        pygame.display.flip()

        # Animation pulse
        pulse_scale += 0.01 * pulse_direction
        if pulse_scale > 1.2:
            pulse_direction = -1
        elif pulse_scale < 0.9:
            pulse_direction = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False

        clock.tick(60)
