import pygame
import pygame.freetype


class PlayerSetupMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.clock = pygame.time.Clock()

        # Chargement de l'arrière-plan
        self.background = pygame.image.load('resources/assets/images/background.jpeg')
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))

        self.state = "choose_players"  # étapes : choose_players → show_controls → enter_names → done
        self.nb_joueurs = None
        self.prenoms = []
        self.error_message = ""
        self.active_input = 0

        self.input_boxes = []
        self.init_input_boxes()

    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf, test_rect = self.font.render(test_line, (255, 255, 255))

            if test_rect.width <= max_width:
                current_line.append(word)
                current_width = test_rect.width
            else:
                if current_line:  # Évite les lignes vides
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_surf, current_rect = self.font.render(word, (255, 255, 255))
                    current_width = current_rect.width
                else:
                    # Un mot trop long est coupé
                    lines.append(word)
                    current_line = []
                    current_width = 0

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def draw_blurred_background(self):
        """ Crée un effet de flou sur l'arrière-plan """
        blurred_background = pygame.transform.smoothscale(self.background, (128, 72))
        blurred_background = pygame.transform.smoothscale(blurred_background, self.screen.get_size())
        self.screen.blit(blurred_background, (0, 0))

    def init_input_boxes(self):
        screen_width, screen_height = self.screen.get_size()
        self.input_boxes = [
            pygame.Rect(screen_width // 2 - 150, screen_height // 2, 300, 50)
        ]
        self.text_input = ""

    def validate_players(self):
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
        modal_width = 700
        modal_height = 500
        modal_x = (screen_width - modal_width) // 2
        modal_y = (screen_height - modal_height) // 2

        self.input_boxes = []

        # Estimer la largeur des labels
        max_label_width = 0
        for i in range(self.nb_joueurs):
            label_text = f"Joueur {i + 1} :"
            label_surf, label_rect = self.font.render(label_text, (255, 255, 255))
            if label_rect.width > max_label_width:
                max_label_width = label_rect.width

        # Dimensions des champs de saisie
        box_width = 300
        box_height = 50

        # Espace total requis par élément (label + espace + input)
        total_width = max_label_width + 20 + box_width

        # Calculer la position verticale centrale dans le modal
        center_y = modal_y + modal_height // 2 - ((self.nb_joueurs * box_height + (self.nb_joueurs - 1) * 30) // 2)

        for i in range(self.nb_joueurs):
            # Centrer horizontalement l'ensemble label + input dans le modal
            x = modal_x + (modal_width - total_width) // 2 + max_label_width + 20
            # Positionner verticalement avec un espacement
            y = center_y + i * (box_height + 30)

            rect = pygame.Rect(x, y, box_width, box_height)
            self.input_boxes.append(rect)

        # Stocker la largeur des labels et position de départ pour l'affichage
        self.label_width = max_label_width
        self.label_start_x = modal_x + (modal_width - total_width) // 2

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

    def draw_modal(self):
        screen_width, screen_height = self.screen.get_size()

        modal_width = 700
        modal_height = 500
        modal_x = (screen_width - modal_width) // 2
        modal_y = (screen_height - modal_height) // 2
        modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)

        modal_surface = pygame.Surface((modal_width, modal_height), pygame.SRCALPHA)
        pygame.draw.rect(modal_surface, (19, 25, 30, 230), modal_surface.get_rect(), border_radius=15)
        self.screen.blit(modal_surface, modal_rect)

        return modal_rect

    def draw_player_setup(self):
        self.draw_blurred_background()
        modal_rect = self.draw_modal()

        # Titre
        title_text = ""
        if self.state == "choose_players":
            title_text = "Combien de joueurs ? (1 ou 2)"
        elif self.state == "show_controls":
            title_text = "Commandes du jeu"
        elif self.state == "enter_names":
            title_text = "Entrez les prénoms des joueurs"

        title_surface, title_rect = self.font.render(title_text, (255, 255, 255))
        title_x = modal_rect.centerx - title_rect.width // 2
        self.screen.blit(title_surface, (title_x, modal_rect.top + 30))

        # Contenu selon l'état
        if self.state == "choose_players":
            input_rect = self.input_boxes[0]
            color = (52, 152, 219) if self.active_input == 0 else (100, 100, 100)
            pygame.draw.rect(self.screen, color, input_rect, 0, border_radius=5)
            pygame.draw.rect(self.screen, (255, 255, 255), input_rect, 2, border_radius=5)

            txt_surface, txt_rect = self.font.render(self.text_input, (255, 255, 255))
            self.screen.blit(txt_surface, (input_rect.x + (input_rect.width - txt_rect.width) // 2,
                                           input_rect.y + (input_rect.height - txt_rect.height) // 2))

        elif self.state == "show_controls":
            instructions = []
            if self.nb_joueurs == 1:
                instructions = [
                    "Mode 1 Joueur :",
                    "- Déplacement : Flèches directionnelles ou ZQSD",
                    "- Canne à pêche : Espace"
                ]
            else:
                instructions = [
                    "Mode 2 Joueurs :",
                    "- Joueur 1 : ZQSD pour se déplacer, A pour pêcher",
                    "- Joueur 2 : Flèches pour se déplacer, M pour pêcher"
                ]

            y_pos = modal_rect.top + 100
            # Largeur maximale pour le texte (avec une marge)
            max_text_width = modal_rect.width - 80

            for instruction in instructions:
                wrapped_lines = self.wrap_text(instruction, max_text_width)
                for line in wrapped_lines:
                    text_surf, text_rect = self.font.render(line, (255, 255, 255))
                    x_pos = modal_rect.centerx - text_rect.width // 2
                    self.screen.blit(text_surf, (x_pos, y_pos))
                    y_pos += 35  # Réduit l'espacement entre les lignes

        elif self.state == "enter_names":
            # Labels pour les joueurs
            for i, box in enumerate(self.input_boxes):
                label_text = f"Joueur {i + 1} :"
                label_surf, label_rect = self.font.render(label_text, (255, 255, 255))
                # Utiliser la position de départ calculée dans init_name_inputs
                self.screen.blit(label_surf, (self.label_start_x, box.y + 10))

                # Champs de saisie
                color = (52, 152, 219) if i == self.active_input else (100, 100, 100)
                pygame.draw.rect(self.screen, color, box, 0, border_radius=5)
                pygame.draw.rect(self.screen, (255, 255, 255), box, 2, border_radius=5)

                txt_surf, _ = self.font.render(self.prenoms[i], (255, 255, 255))
                self.screen.blit(txt_surf, (box.x + 10, box.y + (box.height - txt_surf.get_height()) // 2))

        # Message d'erreur
        if self.error_message:
            error_surf, error_rect = self.font.render(self.error_message, (255, 100, 100))
            error_x = modal_rect.centerx - error_rect.width // 2
            error_y = modal_rect.bottom - 100
            self.screen.blit(error_surf, (error_x, error_y))

        # Bouton de validation
        button_text = ""
        if self.state == "choose_players":
            button_text = "Valider"
        elif self.state == "show_controls":
            button_text = "Continuer"
        elif self.state == "enter_names":
            button_text = "Jouer"

        if button_text:
            # Calculer la taille du texte pour adapter le bouton
            text_surf, text_rect = self.font.render(button_text, (255, 255, 255))
            button_width = max(200, text_rect.width + 40)  # Au moins 200px ou taille du texte + marge
            button_height = 50

            button_rect = pygame.Rect(modal_rect.centerx - button_width // 2,
                                      modal_rect.bottom - 80,
                                      button_width, button_height)
            pygame.draw.rect(self.screen, (46, 204, 113), button_rect, border_radius=10)

            # Centrer le texte dans le bouton
            text_x = button_rect.centerx - text_rect.width // 2
            text_y = button_rect.centery - text_rect.height // 2
            self.screen.blit(text_surf, (text_x, text_y))

        return None

    def run(self):
        running = True

        while running and self.state != "done":
            self.screen.fill((0, 0, 0))
            button_rect = self.draw_player_setup()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return None, None

                    elif event.key == pygame.K_TAB and self.state == "enter_names":
                        # Navigation entre les champs
                        self.active_input = (self.active_input + 1) % len(self.input_boxes)

                    elif event.key == pygame.K_RETURN:
                        if self.state == "choose_players":
                            self.validate_players()
                        elif self.state == "show_controls":
                            self.state = "enter_names"
                            self.init_name_inputs()
                        elif self.state == "enter_names" and self.validate_names():
                            self.state = "done"

                    elif event.key == pygame.K_BACKSPACE:
                        if self.state == "choose_players":
                            self.text_input = self.text_input[:-1]
                        elif self.state == "enter_names":
                            self.prenoms[self.active_input] = self.prenoms[self.active_input][:-1]

                    elif self.state in ["choose_players", "enter_names"]:
                        # Filtrer pour n'accepter que les chiffres dans le premier écran
                        if self.state == "choose_players" and event.unicode.isdigit():
                            self.text_input += event.unicode
                        # Accepter les caractères pour les noms
                        elif self.state == "enter_names":
                            self.prenoms[self.active_input] += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Vérifier si un bouton a été cliqué
                    if button_rect and button_rect.collidepoint(event.pos):
                        if self.state == "choose_players":
                            self.validate_players()
                        elif self.state == "show_controls":
                            self.state = "enter_names"
                            self.init_name_inputs()
                        elif self.state == "enter_names" and self.validate_names():
                            self.state = "done"

                    # Vérifier si un champ de saisie a été cliqué
                    if self.state == "enter_names":
                        for i, box in enumerate(self.input_boxes):
                            if box.collidepoint(event.pos):
                                self.active_input = i

            pygame.display.flip()
            self.clock.tick(60)

        return self.nb_joueurs, self.prenoms
