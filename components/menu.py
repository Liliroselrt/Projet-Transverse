import pygame
import pygame.freetype
import os
from components.game import run_game
from utils.utils import *
from components.historique import *


from components.game import *
from components.setupMenu import *



class Menu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.show_menu = True
        self.show_rules = False
        self.show_historique = False
        
        # Charge les images
        self.background = pygame.image.load('resources/assets/images/background.jpeg')
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))

        self.rules_background = pygame.image.load('resources/assets/images/FondRegle.jpg')
        self.rules_background = pygame.transform.scale(self.rules_background, (screen.get_width(), screen.get_height()))

        # Charge la police d'écriture
        pygame.freetype.init()
        font_path = os.path.join('resources', 'fonts', 'AutourOne.ttf')
        self.font = pygame.freetype.Font(font_path, 36)

    def draw_blurred_background(self):
        """ Creates a blur effect on the background """
        blurred_background = pygame.transform.smoothscale(self.background, (128, 72))
        blurred_background = pygame.transform.smoothscale(blurred_background, self.screen.get_size())
        self.screen.blit(blurred_background, (0, 0))

    def draw_menu(self):
        """ Displays the main menu with Play, Rules, and Quit buttons """
        self.draw_blurred_background()

        screen_width, screen_height = self.screen.get_size()

        modal_width = 600
        modal_height = 350
        modal_x = (screen_width - modal_width) // 2
        modal_y = (screen_height - modal_height) // 2

        modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
        modal_surface = pygame.Surface((modal_width, modal_height), pygame.SRCALPHA)
        pygame.draw.rect(modal_surface, (20, 20, 20, 230), modal_surface.get_rect(), border_radius=15)
        self.screen.blit(modal_surface, modal_rect)

        # Titre
        title_font = pygame.freetype.Font(self.font.path, 60)
        title_surface, _ = title_font.render("Trash & Splash", (255, 255, 255))
        title_x = modal_x + (modal_width - title_surface.get_width()) // 2
        self.screen.blit(title_surface, (title_x, modal_y + 20))

        # Dimensions des boutons
        button_width = 200
        button_height = 60
        spacing = 20

        # Position du premier bouton
        title_height = title_surface.get_height()
        first_button_y = modal_y + title_height + 40

        # Bouton Jouer
        play_button = pygame.Rect(modal_x + (modal_width - button_width) // 2, first_button_y, button_width,
                                  button_height)
        pygame.draw.rect(self.screen, (46, 204, 113), play_button, border_radius=10)

        # Bouton Historique
        histo_button = pygame.Rect(modal_x + (modal_width - button_width) // 2, first_button_y + 1 * (button_height + spacing), button_width, button_height)
        pygame.draw.rect(self.screen, (241, 196, 15), histo_button, border_radius=10)
        
        # Bouton Règles
        rules_button = pygame.Rect(modal_x + (modal_width - button_width) // 2,
                                   first_button_y + 2 * (button_height + spacing), button_width, button_height)
        pygame.draw.rect(self.screen, (52, 152, 219), rules_button, border_radius=10)

        # Bouton Quitter
        quit_button = pygame.Rect(modal_x + (modal_width - button_width) // 2,
                                  first_button_y + 3 * (button_height + spacing), button_width, button_height)
        pygame.draw.rect(self.screen, (231, 76, 60), quit_button, border_radius=10)

        # Bouton text
        solo_text, _ = self.font.render("JOUER", (255, 255, 255))
        historique_text, _ = self.font.render("HISTORIQUE", (0, 0, 0))
        regles_text, _ = self.font.render("RÈGLES", (255, 255, 255))
        quitter_text, _ = self.font.render("QUITTER", (255, 255, 255))

        # Texte centré dans chaque bouton
        self.screen.blit(solo_text,
                         (play_button.x + (button_width - solo_text.get_width()) // 2,
                          play_button.y + (button_height - solo_text.get_height()) // 2))
        self.screen.blit(historique_text, (histo_button.x + (button_width - historique_text.get_width()) // 2,
                                           histo_button.y + (button_height - historique_text.get_height()) // 2))
        self.screen.blit(regles_text, (rules_button.x + (button_width - regles_text.get_width()) // 2,
                                       rules_button.y + (button_height - regles_text.get_height()) // 2))
        self.screen.blit(quitter_text, (quit_button.x + (button_width - quitter_text.get_width()) // 2,
                                        quit_button.y + (button_height - quitter_text.get_height()) // 2))

        return play_button, histo_button, rules_button, quit_button

    def draw_rules(self):
        """ Displays game rules and return button """
        self.screen.blit(self.rules_background, (0, 0))

        screen_width = self.screen.get_width()

        # Titre
        title_text, title_rect = self.font.render("Voici les règles du jeu :", (255, 255, 255))
        title_x = (screen_width - title_rect.width) // 2
        self.screen.blit(title_text, (title_x, 100))

        # Liste des règles
        rules = [
            "1. Attraper les déchets pour sauver les poissons !",
            "2. Attention, vous perdez des points\n",
            " si vous attrapez des poissons",
            "3. Gagnez le jeu en faisant un maximum de points"
        ]

        y_base = 200
        for rule in rules:
            text_surface, rect = self.font.render(rule, (255, 255, 255))
            x = (screen_width - rect.width) // 2
            self.screen.blit(text_surface, (x, y_base))
            y_base += 50

        # Bouton retour
        back_button = pygame.Rect(540, y_base + 50, 200, 50)
        pygame.draw.rect(self.screen, (231, 76, 60), back_button, border_radius=10)
        pygame.draw.rect(self.screen, (192, 57, 43), back_button, 2, border_radius=10)

        text_surface, _ = self.font.render("Retour", (255, 255, 255))
        text_x = back_button.x + (back_button.width - text_surface.get_width()) // 2
        text_y = back_button.y + (back_button.height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))

        return back_button

    def run(self):
        """ Main menu loop """
        while self.running:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.show_menu = True
                    self.show_rules = False
                    self.show_historique = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_menu:
                        play_button, histo_button, rules_button, quit_button = self.draw_menu()

                        if play_button.collidepoint(event.pos):
                            # Lance le menu de configuration des joueurs
                            player_setup = PlayerSetupMenu(self.screen, self.font, 1)
                            nb_joueurs, prenoms = player_setup.run()

                            if nb_joueurs is not None and prenoms:
                                quit_game = run_game(self.screen, self.clock, nb_joueurs, prenoms)
                                if quit_game:
                                    self.running = False
                                    return False
                                self.show_menu = True
                                
                        elif histo_button.collidepoint(event.pos):
                            afficher_historique(self.screen, self.font)
                            self.show_menu = True
                             
                        elif rules_button.collidepoint(event.pos):
                            self.show_menu = False
                            self.show_rules = True

                        elif quit_button.collidepoint(event.pos):
                            self.running = False
                            return False

                    elif self.show_rules:
                        back_button = self.draw_rules()
                        if back_button.collidepoint(event.pos):
                            self.show_rules = False
                            self.show_menu = True

            if self.show_menu:
                self.draw_menu()
            elif self.show_rules:
                self.draw_rules()

            pygame.display.flip()
            self.clock.tick(60)

        return False
