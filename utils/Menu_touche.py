import pygame
import pygame.freetype

class PlayerSetupMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.state = "choose_players"  # étapes : choose_players → show_controls → enter_names → done
        self.input_boxes = []
        self.nb_joueurs = None
        self.prenoms = []
        self.error_message = ""

        self.active_input = 0
        self.text_input = ""

        self.init_input_boxes()

    def init_input_boxes(self):
        screen_width, screen_height = self.screen.get_size()
        self.input_boxes = [
            pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        ]
        self.text_input = ""
        self.active_input = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text_input = self.text_input[:-1]
            elif event.key == pygame.K_RETURN:
                self.validate_input()
            else:
                self.text_input += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == "choose_players":
                self.validate_input()
            elif self.state == "show_controls":
                self.state = "enter_names"
                self.init_name_inputs()
            elif self.state == "enter_names":
                if self.validate_names():
                    self.state = "done"

    def validate_input(self):
        try:
            nb = int(self.text_input)
            if nb in [1, 2]:
                self.nb_joueurs = nb
                self.text_input = ""
                self.state = "show_controls"
                self.error_message = ""
            else:
                self.error_message = "Veuillez entrer 1 ou 2 joueurs."
        except ValueError:
            self.error_message = "Entrée invalide. Tapez 1 ou 2."

    def init_name_inputs(self):
        screen_width, screen_height = self.screen.get_size()
        self.input_boxes = []
        for i in range(self.nb_joueurs):
            rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + i * 70, 200, 50)
            self.input_boxes.append(rect)
        self.prenoms = [""] * self.nb_joueurs
        self.active_input = 0
        self.error_message = ""

    def validate_names(self):
        if all(nom.strip() != "" for nom in self.prenoms):
            self.error_message = ""
            return True
        else:
            self.error_message = "Veuillez remplir tous les prénoms."
            return False

    def draw_player_setup(self):
        self.screen.fill((30, 30, 30))
        screen_width, screen_height = self.screen.get_size()

        # Boîte centrale floutée
        modal_width = 600
        modal_height = 400
        modal_rect = pygame.Rect(
            (screen_width - modal_width) // 2,
            (screen_height - modal_height) // 2,
            modal_width, modal_height
        )
        pygame.draw.rect(self.screen, (50, 50, 50), modal_rect, border_radius=10)

        title_text = ""
        y_pos = modal_rect.top + 40

        if self.state == "choose_players":
            title_text = "Combien de joueurs ? (1 ou 2)"
            input_rect = self.input_boxes[0]
            pygame.draw.rect(self.screen, (255, 255, 255), input_rect, 2, border_radius=5)
            txt_surface, _ = self.font.render(self.text_input, (255, 255, 255))
            self.screen.blit(txt_surface, (input_rect.x + 10, input_rect.y + 10))
        elif self.state == "show_controls":
            title_text = "Touches des joueurs :"
            if self.nb_joueurs == 1:
                controls = [
                    "Mode 1 Joueur :",
                    "- Déplacement : Flèches directionnelles ou ZQSD",
                    "- Canne à pêche : Espace"
                ]
            else:
                controls = [
                    "Mode 2 Joueurs :",
                    "Joueur 1 : ZQSD pour bouger, A pour pêcher",
                    "Joueur 2 : Flèches pour bouger, M pour pêcher"
                ]
            for i, line in enumerate(controls):
                text, _ = self.font.render(line, (255, 255, 255))
                self.screen.blit(text, (modal_rect.left + 50, y_pos + i * 40))
            y_pos += len(controls) * 40 + 20

        elif self.state == "enter_names":
            title_text = "Entrez les prénoms des joueurs :"
            for i, box in enumerate(self.input_boxes):
                pygame.draw.rect(self.screen, (255, 255, 255), box, 2, border_radius=5)
                txt_surface, _ = self.font.render(self.prenoms[i], (255, 255, 255))
                self.screen.blit(txt_surface, (box.x + 10, box.y + 10))

        # Affiche le titre principal
        if title_text:
            title_surface, _ = self.font.render(title_text, (255, 255, 255))
            self.screen.blit(title_surface, (
                modal_rect.centerx - title_surface.get_width() // 2,
                modal_rect.top + 20
            ))

        # Affiche le message d'erreur s'il y en a un
        if self.error_message:
            error_surface, _ = self.font.render(self.error_message, (255, 100, 100))
            self.screen.blit(error_surface, (
                modal_rect.centerx - error_surface.get_width() // 2,
                modal_rect.bottom - 60
            ))

        # Affiche un bouton Valider ou Continuer
        button_text = "Valider" if self.state == "choose_players" else \
                      "Continuer" if self.state == "show_controls" else \
                      "Jouer" if self.state == "enter_names" else ""
        if button_text:
            button_rect = pygame.Rect(modal_rect.centerx - 100, modal_rect.bottom - 100, 200, 50)
            pygame.draw.rect(self.screen, (46, 204, 113), button_rect, border_radius=10)
            text_surf, _ = self.font.render(button_text, (255, 255, 255))
            self.screen.blit(text_surf, (
                button_rect.centerx - text_surf.get_width() // 2,
                button_rect.centery - text_surf.get_height() // 2
            ))

        pygame.display.flip()

    def run(self):
        running = True
        while running and self.state != "done":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None, None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Gère la sélection du champ actif
                    if self.state == "enter_names":
                        for i, box in enumerate(self.input_boxes):
                            if box.collidepoint(event.pos):
                                self.active_input = i
                    self.handle_event(event)
                elif event.type == pygame.KEYDOWN:
                    if self.state == "enter_names":
                        if event.key == pygame.K_BACKSPACE:
                            self.prenoms[self.active_input] = self.prenoms[self.active_input][:-1]
                        else:
                            self.prenoms[self.active_input] += event.unicode
                    else:
                        self.handle_event(event)

            self.draw_player_setup()

        return self.nb_joueurs, self.prenoms
