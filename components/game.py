import pygame  # Bibliothèque principale pour le jeu
import random  # Pour générer des valeurs aléatoires
import math  # Pour les calculs trigonométriques
import os  # Pour gérer les chemins de fichiers

from components.fishing import FishingLine

# Configuration des touches pour le joueur 1 (flèches directionnelles + espace)

ARROWS_P1 = dict(left=pygame.K_LEFT, right=pygame.K_RIGHT,
                 up=pygame.K_UP, down=pygame.K_DOWN,
                 cast=pygame.K_SPACE)

# Configuration des touches pour le joueur 2 en disposition AZERTY
AZERTY_P2 = dict(left=pygame.K_q, right=pygame.K_d,
                 up=pygame.K_z, down=pygame.K_s,
                 cast=pygame.K_e)


class Fish:
    def __init__(self, screen_width, screen_height):
        self.speed_x = random.choice([-2, -1, 1, 2])
        self.speed_y = random.uniform(-0.5, 0.5)

        # Charge une image aléatoire d'un poisson
        fish_num = random.randint(1, 18)
        try:
            self.image = pygame.image.load(f'./resources/assets/fishs/{fish_num}.png').convert_alpha()

            # Dimensions originales
            orig_width = self.image.get_width()
            orig_height = self.image.get_height()

            # Calcule l'échelle pour une bonne taille
            target_width = random.randint(50, 90)
            scale_factor = target_width / orig_width

            self.width = target_width
            self.height = int(orig_height * scale_factor)

            self.image = pygame.transform.scale(self.image, (self.width, self.height))

            # Retourner l'image si le poisson se déplace vers la DROITE (et non vers la gauche)
            if self.speed_x > 0:
                self.image = pygame.transform.flip(self.image, True, False)
        except:
            self.image = None
            self.color = random.choice([(255, 165, 0), (0, 255, 255), (255, 0, 255)])
            self.width = random.randint(60, 100)
            self.height = random.randint(30, 50)

        if self.speed_x > 0:
            self.x = -self.width
        else:
            self.x = screen_width

        self.y = random.randint(screen_height // 2, screen_height - 50)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.caught = False
        self.value = random.randint(1, 5)

    def update(self, screen_width, screen_height):
        if not self.caught:
            self.x += self.speed_x
            self.y += self.speed_y

            if random.random() < 0.02:
                self.speed_y = random.uniform(-0.5, 0.5)

            # Maintenir le poisson dans les limites de l'écran
            if self.y < screen_height // 2:
                self.y = screen_height // 2
                self.speed_y *= -1
            elif self.y > screen_height - 50:
                self.y = screen_height - 50
                self.speed_y *= -1

            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            if (self.x < -self.width and self.speed_x < 0) or (self.x > screen_width and self.speed_x > 0):
                return True
        return False

    def draw(self, screen):
        if not self.caught:
            if self.image:
                screen.blit(self.image, (self.x, self.y))
            else:
                pygame.draw.ellipse(screen, self.color, self.rect)
                eye_x = self.x + (self.width - 5) if self.speed_x < 0 else self.x + 5
                pygame.draw.circle(screen, (255, 255, 255), (eye_x, self.y + self.height // 2), 3)


class Trash:
    def __init__(self, screen_width, screen_height):
        self.speed_x = random.choice([-2, -1, 1, 2])
        self.speed_y = random.uniform(-0.5, 0.5)

        # Charge une image aléatoire d'un déchet
        trash_num = random.randint(1, 14)
        try:
            self.image = pygame.image.load(f'./resources/assets/trash/{trash_num}.png').convert_alpha()

            # Dimensions originales
            orig_width = self.image.get_width()
            orig_height = self.image.get_height()

            # Calcule l'échelle pour une bonne taille
            target_width = random.randint(30, 70)
            scale_factor = target_width / orig_width

            self.width = target_width
            self.height = int(orig_height * scale_factor)

            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except:
            self.image = None
            self.color = random.choice([(100, 100, 100), (150, 150, 150), (200, 200, 200)])
            self.width = random.randint(40, 80)
            self.height = random.randint(20, 40)

        if self.speed_x > 0:
            self.x = -self.width
        else:
            self.x = screen_width

        self.y = random.randint(screen_height // 2, screen_height - 50)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.caught = False
        self.value = 1  # Chaque déchet vaut 1 point

    def update(self, screen_width, screen_height):
        if not self.caught:
            self.x += self.speed_x
            self.y += self.speed_y

            if random.random() < 0.02:
                self.speed_y = random.uniform(-0.5, 0.5)

            # Maintenir les déchets dans les limites de l'écran
            if self.y < screen_height // 2:
                self.y = screen_height // 2
                self.speed_y *= -1
            elif self.y > screen_height - 50:
                self.y = screen_height - 50
                self.speed_y *= -1

            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            if (self.x < -self.width and self.speed_x < 0) or (self.x > screen_width and self.speed_x > 0):
                return True
        return False

    def draw(self, screen):
        if not self.caught:
            if self.image:
                screen.blit(self.image, (self.x, self.y))
            else:
                pygame.draw.rect(screen, self.color, self.rect)


class SpecialTrash(Trash):
    def __init__(self, screen_width, screen_height):
        # Vitesse plus élevée horizontalement
        self.speed_x = random.choice([-6, -5.5, 5.5, 6])  # Vitesse doublée
        self.speed_y = random.uniform(-2.0, 2.0)  # Mouvement vertical beaucoup plus vif

        try:
            self.image = pygame.image.load('./resources/assets/trash/special.png').convert_alpha()

            # Dimensions originales
            orig_width = self.image.get_width()
            orig_height = self.image.get_height()

            # Plus petit que les déchets normaux
            target_width = random.randint(20, 40)  # Plus petit
            scale_factor = target_width / orig_width

            self.width = target_width
            self.height = int(orig_height * scale_factor)

            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except:
            self.image = None
            self.color = (255, 215, 0)  # Couleur or pour le distinguer
            self.width = random.randint(20, 40)
            self.height = random.randint(15, 30)

        if self.speed_x > 0:
            self.x = -self.width
        else:
            self.x = screen_width

        self.y = random.randint(screen_height // 2, screen_height - 50)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.caught = False
        self.value = 50  # 50 points pour un déchet spécial

    def update(self, screen_width, screen_height):
        if not self.caught:
            self.x += self.speed_x
            self.y += self.speed_y

            # Changements de direction plus fréquents
            if random.random() < 0.04:  # Probabilité plus élevée de changer de direction
                self.speed_y = random.uniform(-0.8, 0.8)

            # Maintenir les déchets dans les limites de l'écran
            if self.y < screen_height // 2:
                self.y = screen_height // 2
                self.speed_y *= -1
            elif self.y > screen_height - 50:
                self.y = screen_height - 50
                self.speed_y *= -1

            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            if (self.x < -self.width and self.speed_x < 0) or (self.x > screen_width and self.speed_x > 0):
                return True
        return False


class Player:
    def __init__(self, screen_width, screen_height, start_x=None, controls=None, name=""):
        self.screen_width = screen_width  # Stocke largeur écran
        self.screen_height = screen_height  # Stocke hauteur écran
        self.controls = controls or ARROWS_P1  # défaut : les flèches
        self.name = name  # Nom du joueur pour l'affichage des scores

        # image du bateau
        self.boat_img = pygame.image.load('./resources/assets/barque.png').convert_alpha()
        self.boat_img = pygame.transform.scale(self.boat_img, (120, 60))

        # position initiale
        if start_x is None:
            self.boat_x = screen_width // 2 - self.boat_img.get_width() // 2
        else:
            self.boat_x = start_x
        self.boat_y = screen_height // 3

        # Définir la position de la canne avant de créer la ligne de pêche
        self.rod_x = self.boat_x + self.boat_img.get_width() // 2
        self.rod_y = self.boat_y  # Canne positionnée au sommet du bateau

        self.fishing_line = FishingLine(self.rod_x, self.rod_y, screen_height - self.boat_y - 20, self.boat_y)
        self.is_fishing = False
        self.score = 0

        self.font = pygame.freetype.Font(os.path.join('resources', 'fonts', 'AutourOne.ttf'), 18)

    def move(self, keys):
        # Deplacement du bateau de droite à guauche
        if keys[self.controls['left']] and self.boat_x > 0:
            self.boat_x -= 3
        if keys[self.controls['right']] and self.boat_x < self.screen_width - self.boat_img.get_width():
            self.boat_x += 3

        self.rod_x = self.boat_x + self.boat_img.get_width() // 2  # Met à jour la position de la canne

        # Ajoutez le réglage de l'angle avec les touches UP/DOWN
        if not self.is_fishing:  # Vérifier que le joueur ne pêche pas
            if keys[self.controls['up']]:
                self.fishing_line.adjust_angle(1)  # Augmenter l'angle
            if keys[self.controls['down']]:
                self.fishing_line.adjust_angle(-1)  # Diminuer l'angle

    def cast_line(self):
        self.is_fishing = not self.is_fishing  # Alterne ente lancer/retracter

    def update_line(self):
        # Met à jour la position de l'ameçon
        self.fishing_line.update(self.rod_x, self.rod_y, self.is_fishing, 1 / 60)  # En supposant 60 FPS

    def get_hook_position(self):
        # Coordonnées du crochet
        return self.fishing_line.get_hook_position()

    def draw(self, screen):
        # Le bateau
        screen.blit(self.boat_img, (self.boat_x, self.boat_y))

        # Dessiner l'indicateur d'angle si le joueur ne pêche pas
        if not self.is_fishing:
            self.draw_angle_indicator(screen)

        # Dessiner la ligne de pêche
        self.fishing_line.draw(screen)

    def draw_angle_indicator(self, screen):
        # Dessiner une ligne rouge pour indiquer l'angle de la canne à pêche
        angle_rad = self.fishing_line.angle_rad
        line_length = 30  # Longueur de la ligne indicatrice
        end_x = self.rod_x + line_length * math.cos(angle_rad)
        end_y = self.rod_y - line_length * math.sin(angle_rad)

        # Affiche l'indicateur d'angle
        pygame.draw.line(screen, (255, 0, 0), (self.rod_x, self.rod_y), (end_x, end_y), 2)

        # Affiche le texte de l'angle
        self.font.render_to(screen, (self.rod_x - 40, self.rod_y - 20), f"{int(self.fishing_line.angle_degrees)}°",
                            (255, 255, 255))


class Game:
    def __init__(self, screen_width=1280, screen_height=720, players=None):
        # stocke la hauteur et la largeur de la fenêtre
        self.screen_width = screen_width
        self.screen_height = screen_height
        if players is None:
            self.players = [Player(screen_width, screen_height,
                                   start_x=screen_width // 2, controls=ARROWS_P1)]  # Liste des joueurs
        else:
            # liste des poisson et des déchets
            self.players = players
        self.fishes = []
        self.trashes = []
        self.special_trashes = []
        self.score = 0
        self.game_time = 1  # 90s de jeu
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.freetype.Font(os.path.join('resources', 'fonts', 'AutourOne.ttf'), 24)
        self.background = pygame.image.load('resources/assets/images/background.jpeg')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

        # La musique
        self.volume = 0.5  # Volume à 50%
        if not pygame.mixer.music.get_busy():
            pygame.mixer.init()
            pygame.mixer.music.load('resources/sound/music.mp3')
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)  # Répéter en boucle indéfiniment

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000  # Temps écoulé en secondes
        remaining_time = max(0, self.game_time - elapsed_time)  # Temps restant

        keys = pygame.key.get_pressed()  # État de toutes les touches
        for p in self.players:
            p.move(keys)  # Déplace chaque joueur
            p.update_line()  # Met à jour la canne

        # Ajoute des poissons aléatoirement
        if len(self.fishes) < 10 and random.random() < 0.02:
            self.fishes.append(Fish(self.screen_width, self.screen_height))

        # Ajoute des déchets aléatoirement
        if len(self.trashes) < 8 and random.random() < 0.02:
            self.trashes.append(Trash(self.screen_width, self.screen_height))

        # Ajoute des déchets spéciaux rarement
        if len(self.special_trashes) < 1 and random.random() < 0.001:  # Probabilité plus faible
            self.special_trashes.append(SpecialTrash(self.screen_width, self.screen_height))

        # Regarde si le poisson ou un déchet est attrapé

        for fish in self.fishes[:]:
            for p in self.players:
                if p.is_fishing and fish.rect.collidepoint(*p.fishing_line.hook_pos):
                    p.score -= 1  # Pert 1 point par poisson
                    self.fishes.remove(fish)  # Suppression du poisson
                    break
            else:
                if fish.update(self.screen_width, self.screen_height):
                    self.fishes.remove(fish)  # Suppression si hors-écran

        for trash in self.trashes[:]:
            if trash.update(self.screen_width, self.screen_height):
                self.trashes.remove(trash)
                continue
            for p in self.players:
                if p.is_fishing and trash.rect.collidepoint(*p.fishing_line.hook_pos):
                    trash.caught = True
                    p.score += 3  # Gagne 3 points par déchet
                    self.trashes.remove(trash)
                    break

        for special in self.special_trashes[:]:
            if special.update(self.screen_width, self.screen_height):
                self.special_trashes.remove(special)
                continue
            for p in self.players:
                if p.is_fishing and special.rect.collidepoint(*p.fishing_line.hook_pos):
                    special.caught = True
                    p.score += 50  # Gagne 50 points pour un déchet spécial
                    self.special_trashes.remove(special)
                    break

        return remaining_time == 0  # Retourne True si le temps est écoulé

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for p in self.players:
            p.draw(screen)

        # Position horizontale commune pour tous les affichages
        x_pos = 10
        y_base = 10

        # Affichage des scores des joueurs
        for p in self.players:
            txt, _ = self.font.render(f"{p.name} : {p.score}", (0, 0, 0))
            screen.blit(txt, (x_pos, y_base))
            y_base += txt.get_height() + 5

        # Calcul de la position pour le temps restant (sous les scores des joueurs)
        time_y = y_base + 10  # 10px d'espace supplémentaire

        # Affiche les poissons
        for fish in self.fishes:
            fish.draw(screen)

        # Affiche les déchets
        for trash in self.trashes:
            trash.draw(screen)

        # Affiche les déchets spéciaux
        for special in self.special_trashes:
            special.draw(screen)

        # Affiche le temps restant aligné avec les scores des joueurs
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000
        remaining_time = max(0, self.game_time - elapsed_time)

        self.font.render_to(screen, (x_pos, time_y), f"Time: {remaining_time}", (0, 0, 0))

    def end_game(self, screen):
        """Affiche l'écran de fin de jeu et gère le retour au menu"""
        game_over_screen = GameOver(screen.get_width(), screen.get_height())
        game_over_screen.run(screen, self.players)


def run_game(screen, clock, nbjoueur, prenoms, versus=False):
    w, h = screen.get_width(), screen.get_height()  # Récupère dimensions de la fenêtre
    players = [Player(w, h, start_x=150, controls=ARROWS_P1, name=prenoms[0])]  # Création joueur 1
    if nbjoueur == 2 or versus:
        players.append(Player(w, h, start_x=w - 150, controls=AZERTY_P2, name=prenoms[1]))  # Création joueur 2
    game = Game(w, h, players)  # Instanciation du jeu
    game_over = False  # Boucle tant que partie non terminée

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True  # quitter completement
            if event.type == pygame.KEYDOWN:
                for p in players:
                    if event.key == p.controls['cast']:
                        p.cast_line()  # Lance ou rétracte la ligne

                if event.key == pygame.K_ESCAPE:
                    return False  # retour au menu

        game_over = game.update()  # Logique de mise à jour
        game.draw(screen)  # Rendu graphique
        pygame.display.flip()  # Affiche la frame
        clock.tick(60)  # Limite à 60 FPS

    try:
        for p in players:
            save_score(p.name, p.score)  # sauvegarde
    except Exception as e:
        print(f"[WARN] Impossible d’enregistrer le score : {e}")

    for p in players:
        save_score(p.name, p.score)

    # Écran de Game Over
    game.end_game(screen)
    return False
