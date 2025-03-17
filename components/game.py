import pygame
import random
import os


class Fish:
    def __init__(self, screen_width, screen_height):
        self.speed_x = random.choice([-2, -1, 1, 2])
        self.speed_y = random.uniform(-0.5, 0.5)

        # Charge une image aléatoire d'un poisson
        fish_num = random.randint(1, 18)
        try:
            self.image = pygame.image.load(f'./resources/assets/fishs/{fish_num}.png').convert_alpha()

            # Original dimensions
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

            # Keep fish within screen bounds
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


class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.boat_img = pygame.image.load('./resources/assets/barque.png').convert_alpha()
        self.boat_img = pygame.transform.scale(self.boat_img, (120, 60))
        self.boat_x = screen_width // 2 - self.boat_img.get_width() // 2
        self.boat_y = screen_height // 3

        # Cane à pêche
        self.rod_x = self.boat_x + self.boat_img.get_width() // 2
        self.rod_y = self.boat_y
        self.line_length = 0
        self.max_line_length = screen_height - self.boat_y - 20
        self.is_fishing = False
        self.score = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.boat_x > 0:
            self.boat_x -= 3
        if keys[pygame.K_RIGHT] and self.boat_x < self.screen_width - self.boat_img.get_width():
            self.boat_x += 3

        self.rod_x = self.boat_x + self.boat_img.get_width() // 2

    def cast_line(self, keys):
        if keys[pygame.K_SPACE]:
            self.is_fishing = True

        if self.is_fishing:
            if self.line_length < self.max_line_length:
                self.line_length += 5

        if keys[pygame.K_UP]:
            self.is_fishing = False
            self.line_length = 0

    def get_hook_position(self):
        return (self.rod_x, self.rod_y + self.line_length)

    def draw(self, screen):
        # Le bateau
        screen.blit(self.boat_img, (self.boat_x, self.boat_y))

        # La câne à pêche
        pygame.draw.line(screen, (139, 69, 19), (self.rod_x, self.rod_y),
                         (self.rod_x, self.rod_y + self.line_length), 2)

        if self.is_fishing and self.line_length > 0:
            hook_x, hook_y = self.get_hook_position()
            pygame.draw.circle(screen, (192, 192, 192), (hook_x, hook_y), 5)


class Game:
    def __init__(self, screen_width=1280, screen_height=720):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = Player(screen_width, screen_height)
        self.fishes = []
        self.score = 0
        self.game_time = 60  # 60s de jeu
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.freetype.Font(os.path.join('resources', 'fonts', 'AutourOne.ttf'), 24)
        self.background = pygame.image.load('./resources/background.jpeg')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000
        remaining_time = max(0, self.game_time - elapsed_time)

        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.cast_line(keys)

        # Ajoute des poissons aléatoirement
        if len(self.fishes) < 10 and random.random() < 0.02:
            self.fishes.append(Fish(self.screen_width, self.screen_height))

        # Regarde si le poisson est attrapé
        hook_pos = self.player.get_hook_position()
        hook_rect = pygame.Rect(hook_pos[0] - 5, hook_pos[1] - 5, 10, 10)

        for fish in self.fishes[:]:
            if fish.update(self.screen_width, self.screen_height):
                self.fishes.remove(fish)
            elif self.player.is_fishing and hook_rect.colliderect(fish.rect) and not fish.caught:
                fish.caught = True
                self.score += fish.value
                self.fishes.remove(fish)

        return remaining_time == 0  # Retourne True si le temps est écoulé

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.player.draw(screen)

        # Affiche les poissons
        for fish in self.fishes:
            fish.draw(screen)

        # Affiche le score et le temps restant
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000
        remaining_time = max(0, self.game_time - elapsed_time)

        self.font.render_to(screen, (20, 20), f"Score: {self.score}", (255, 255, 255))
        self.font.render_to(screen, (20, 50), f"Time: {remaining_time}", (255, 255, 255))


def run_game(screen, clock):
    game = Game(screen.get_width(), screen.get_height())
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        game_over = game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    # Ecran de Game Over
    font = pygame.freetype.Font(os.path.join('resources', 'fonts', 'AutourOne.ttf'), 48)
    game_over_text = f"Game Over! Score: {game.score}"

    text_rect = font.get_rect(game_over_text)
    text_x = (screen.get_width() - text_rect.width) // 2
    text_y = (screen.get_height() - text_rect.height) // 2

    font.render_to(screen, (text_x, text_y), game_over_text, (255, 255, 255))

    pygame.display.flip()
    pygame.time.delay(3000)

    return False
