import pygame
import pygame.freetype
import os


class GameOver:
    def __init__(self, screen_width, screen_height):
        # Dimensions de l'écran pour positionner les éléments
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Chargement et mise à l'échelle du fond d'écran
        self.background = pygame.image.load('resources/assets/images/background.jpeg')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
         # Chargement de la police personnalisée pour titre et texte
        font_path = os.path.join('resources', 'fonts', 'AutourOne.ttf')
        self.font_title = pygame.freetype.Font(font_path, 100)    # Police pour le titre
        self.font_text = pygame.freetype.Font(font_path, 60)    # Police pour le texte courant
        
        # Paramètres pour l'effet de pulsation sur le texte du gagnant
        self.pulse_scale = 1.0    # Échelle actuelle de la police
        self.pulse_direction = 1    # Direction de changement (+1 ou -1)
        self.clock = pygame.time.Clock()    # Horloge pour réguler le rafraîchissement

    def draw_text_with_shadow(self, surface, text, font, color, x, y, shadow_color=(0, 0, 0), offset=2):
        # Dessine d'abord l'ombre décalée
        font.render_to(surface, (x + offset, y + offset), text, shadow_color)
        text_rect = font.get_rect(text)    # Récupère la taille du texte pour positionnement
        font.render_to(surface, (x, y), text, color)    # Dessine le texte principal
        return text_rect

    def run(self, screen, players):
        # Détecte gagnant si 2 joueurs
        winner = None
        if len(players) == 2:
            if players[0].score > players[1].score:
                winner = players[0]
            elif players[1].score > players[0].score:
                winner = players[1]
            else:
                winner = None  # Égalité

        running = True
        continue_btn_rect = None    # Rectangle cliquable pour continuer

        while running:
            # Gestion des événements
            for event in pygame.event.get():
                 # Si clic sur le bouton "continuer"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_btn_rect and continue_btn_rect.collidepoint(event.pos):
                        return False    # Sortie de l'écran Game Over

            # Affichage
            screen.blit(self.background, (0, 0))

            # Titre
            title_text = "GAME OVER !"
            title_rect = self.font_title.get_rect(title_text)
            self.draw_text_with_shadow(
                screen, title_text, self.font_title, (255, 255, 255),
                self.screen_width // 2 - title_rect.width // 2, 80
            )

            # Affichage des scores
            y_offset = 250
            for p in players:
                text = f"{p.name} : {p.score} pts"

                if (winner and p == winner) or (len(players) == 1):  # Gagnant ou joueur solo
                    # Créer une police temporaire avec pulsation
                    temp_font = pygame.freetype.Font(os.path.join('resources', 'fonts', 'AutourOne.ttf'),
                                                     int(60 * self.pulse_scale))
                    text_rect = temp_font.get_rect(text)
                    # Texte doré pour le gagnant
                    self.draw_text_with_shadow(
                        screen, text, temp_font, (255, 215, 0),
                        self.screen_width // 2 - text_rect.width // 2, y_offset
                    )
                else:
                    # Texte gris pour les autres joueurs
                    text_rect = self.font_text.get_rect(text)
                    self.draw_text_with_shadow(
                        screen, text, self.font_text, (200, 200, 200),
                        self.screen_width // 2 - text_rect.width // 2, y_offset
                    )
                y_offset += 100    # Espace vertical entre les lignes de score

            # Instructions pour continuer
            quit_text = "Appuyez ici pour continuer"
            quit_rect = self.font_text.get_rect(quit_text)
            x_pos = self.screen_width // 2 - quit_rect.width // 2
            y_pos = self.screen_height - 120

            # Créer un rectangle plus grand pour la zone cliquable
            continue_btn_rect = pygame.Rect(x_pos - 20, y_pos - 10, quit_rect.width + 40, quit_rect.height + 20)

            # Dessiner un fond pour le bouton
            pygame.draw.rect(screen, (0, 100, 150), continue_btn_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 150, 200), continue_btn_rect, width=3, border_radius=10)
            
            # Texte du bouton avec ombre
            self.draw_text_with_shadow(
                screen, quit_text, self.font_text, (255, 255, 255),
                x_pos, y_pos
            )

            # Animation pulse
            self.pulse_scale += 0.01 * self.pulse_direction
            if self.pulse_scale > 1.2:
                self.pulse_direction = -1
            elif self.pulse_scale < 0.9:
                self.pulse_direction = 1
                
            # Rafraîchissement de l'écran et limitation FPS
            pygame.display.flip()
            self.clock.tick(60)
        return None    # Valeur de retour si on sort autrement
