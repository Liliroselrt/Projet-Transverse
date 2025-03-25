import pygame
import math


class FishingLine:
    def __init__(self, rod_x, rod_y, max_length, boat_y):
        self.rod_x = rod_x
        self.rod_y = rod_y
        self.max_length = max_length
        self.current_length = 0
        self.is_casting = False
        self.segments = 20  # Nombre de segments de ligne pour une courbe plus lisse
        self.hook_x = rod_x
        self.hook_y = rod_y

        # Paramètres physiques
        self.gravity = 9.81
        self.initial_velocity = 60.0
        self.angle_degrees = 60
        self.angle_rad = math.radians(60)  # Angle de lancement de 60 degrés

        # Paramètres de la ligne d'eau (coordonnée y où l'eau commence)
        self.water_level = boat_y + 30
        self.hook_in_water = False
        self.water_entry_x = rod_x
        self.sinking_speed = 4.5
        self.sinking_depth = 0

        # Paramètres de transition pour l'entrée dans l'eau
        self.water_transition = 0.0  # 0.0 = air, 1.0 = complètement dans l'eau
        self.transition_speed = 0.1  # Vitesse de la transition

    def set_angle(self, angle_degrees):
        # Limitez l'angle entre 30 et 80 degrés pour une pêche réaliste.
        self.angle_degrees = max(30, min(80, angle_degrees))
        self.angle_rad = math.radians(self.angle_degrees)

    def adjust_angle(self, delta):
        # Ne permettre le réglage de l'angle que lorsque l'on ne pêche pas
        if not self.is_casting:
            self.set_angle(self.angle_degrees + delta)

    def update(self, rod_x, rod_y, is_casting, delta_time):
        # Calculer le déplacement du bateau/canne à pêche
        rod_movement = rod_x - self.rod_x

        # Mettre à jour la position de la canne
        self.rod_x = rod_x
        self.rod_y = rod_y
        self.is_casting = is_casting

        # Si l'hameçon est dans l'eau et que le bateau bouge, ajuster le point d'entrée dans l'eau
        if self.hook_in_water and rod_movement != 0:
            # Effet d'amortissement pour un mouvement plus réaliste
            dampening = 0.7  # Facteur d'amortissement (0-1)
            self.water_entry_x += rod_movement * dampening
            self.hook_x = self.water_entry_x  # Mettre à jour la position horizontale de l'hameçon

        # Réinitialiser l'état lorsqu'il n'y a pas de lancer
        if not is_casting:
            self.current_length = 0
            self.hook_x = rod_x
            self.hook_y = rod_y
            self.hook_in_water = False
            self.sinking_depth = 0
            self.water_transition = 0.0
            return

        # Mettre à jour la longueur de la ligne lors du lancer
        if is_casting and self.current_length < self.max_length:
            self.current_length += 5
            if self.current_length > self.max_length:
                self.current_length = self.max_length

        # Calculer la position de l'hameçon
        if self.current_length > 0:
            t = (self.current_length / self.max_length) * 2.0

            if not self.hook_in_water:
                x_offset = self.initial_velocity * math.cos(self.angle_rad) * t * 10
                y_offset = self.initial_velocity * math.sin(self.angle_rad) * t * 10 - 0.5 * self.gravity * (
                        t * 10) ** 2

                self.hook_x = self.rod_x + x_offset
                self.hook_y = self.rod_y - y_offset

                if self.hook_y >= self.water_level:
                    self.hook_in_water = True
                    self.water_entry_x = self.hook_x
                    self.hook_y = self.water_level
                    self.water_transition = 0.0  # Démarrer la transition
            else:
                # Mettre à jour la transition
                if self.water_transition < 1.0:
                    self.water_transition = min(self.water_transition + self.transition_speed, 1.0)

                self.hook_x = self.water_entry_x
                self.sinking_depth = min(self.sinking_depth + self.sinking_speed, 450)
                self.hook_y = self.water_level + self.sinking_depth

    def get_hook_position(self):
        return (self.hook_x, self.hook_y)

    def draw(self, screen):
        if self.current_length <= 0:
            return

        # Dessiner la ligne de pêche
        points = []

        # Commencer à la position de la canne
        points.append((self.rod_x, self.rod_y))

        if not self.hook_in_water or self.water_transition < 1.0:
            # Calculer les points pour la trajectoire aérienne
            air_points = [(self.rod_x, self.rod_y)]
            for i in range(1, self.segments):
                segment_t = (i / self.segments) * (self.current_length / self.max_length) * 2.0

                x_offset = self.initial_velocity * math.cos(self.angle_rad) * segment_t * 10
                y_offset = self.initial_velocity * math.sin(self.angle_rad) * segment_t * 10 - 0.5 * self.gravity * (
                        segment_t * 10) ** 2

                x = self.rod_x + x_offset
                y = self.rod_y - y_offset

                air_points.append((x, y))
            air_points.append((self.hook_x, self.hook_y))

            if not self.hook_in_water:
                points = air_points
            else:
                # Calculer les points pour la trajectoire aquatique
                water_points = [(self.rod_x, self.rod_y)]
                water_reached = False
                for i in range(1, self.segments + 1):
                    percent = i / self.segments
                    x = self.rod_x + (self.water_entry_x - self.rod_x) * percent
                    h = min(50, abs(self.water_entry_x - self.rod_x) * 0.2)
                    rel_x = percent - 0.5
                    y = self.rod_y + (self.water_level - self.rod_y) * percent - h * (1 - 4 * rel_x * rel_x)

                    if y > self.water_level and not water_reached:
                        water_reached = True
                        water_points.append((x, self.water_level))
                        break
                    water_points.append((x, y))

                if not water_reached:
                    water_points.append((self.water_entry_x, self.water_level))

                for i in range(1, 5):
                    depth_factor = i / 4
                    water_points.append((self.water_entry_x, self.water_level + self.sinking_depth * depth_factor))
                water_points.append((self.hook_x, self.hook_y))

                # Mélanger les points selon la transition
                points = []
                min_length = min(len(air_points), len(water_points))
                for i in range(min_length):
                    x1, y1 = air_points[i]
                    x2, y2 = water_points[i]
                    x = x1 * (1 - self.water_transition) + x2 * self.water_transition
                    y = y1 * (1 - self.water_transition) + y2 * self.water_transition
                    points.append((x, y))

                # Ajouter les points restants de la liste la plus longue
                if len(air_points) > len(water_points):
                    points.extend(air_points[min_length:])
                elif len(water_points) > len(air_points):
                    points.extend(water_points[min_length:])
        else:
            # Méthode normale de dessin quand l'hameçon est complètement dans l'eau
            water_reached = False
            for i in range(1, self.segments + 1):
                percent = i / self.segments
                x = self.rod_x + (self.water_entry_x - self.rod_x) * percent
                h = min(50, abs(self.water_entry_x - self.rod_x) * 0.2)
                rel_x = percent - 0.5
                y = self.rod_y + (self.water_level - self.rod_y) * percent - h * (1 - 4 * rel_x * rel_x)

                if y > self.water_level and not water_reached:
                    water_reached = True
                    points.append((x, self.water_level))
                    break
                points.append((x, y))

            if not water_reached:
                points.append((self.water_entry_x, self.water_level))

            for i in range(1, 5):
                depth_factor = i / 4
                points.append((self.water_entry_x, self.water_level + self.sinking_depth * depth_factor))
            points.append((self.hook_x, self.hook_y))

        # Dessiner la ligne
        if len(points) > 1:
            pygame.draw.lines(screen, (139, 69, 19), False, points, 2)

        # Dessiner l'hameçon
        if self.current_length > 10:
            hook_pos = (self.hook_x, self.hook_y)
            pygame.draw.circle(screen, (192, 192, 192), hook_pos, 5)
